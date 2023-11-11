from bgp_simulator_pkg import Prefixes, Relationships

from .shortest_path_export_all import ShortestPathExportAll


class Eavesdropper(ShortestPathExportAll):
    """Attacker has visibility into other AS RIBs.
       Vantage points must be defined in subclasses.
    """

    vantage_points = []

    def __init__(self, global_eavesdropper=True, **kwargs):
        super().__init__(**kwargs)
        self.global_eavesdropper = global_eavesdropper

    def post_propagation_hook(self, engine,
                              propagation_round, *args, **kwargs):
        """Add the route leak from the attacker"""
        attacker_ann = None
        attacker_asn = list(self.attacker_asns)[0]
        # Freeze this current ann in the local rib of the attacker
        attacker_ann = engine.as_dict[attacker_asn]._local_rib.get_ann(Prefixes.PREFIX.value) # noqa E501
        if attacker_ann is not None:
            attacker_ann.seed_asn = attacker_asn
            attacker = engine.as_dict[attacker_asn]
        if propagation_round == 0:
            attack_anns = []
            attacker = engine.as_dict[attacker_asn]
            if self.global_eavesdropper:
                vantage_points = list(engine.as_dict.keys())
            else:
                vantage_points = self.vantage_points
            atk_ann_candidates = []
            for asn in [attacker_asn] + vantage_points:
                current_as = engine.as_dict[asn]
                if ((current_as.name == self.AdoptASCls.name or
                     current_as.name == "Pseudo" + self.AdoptASCls.name) and
                        asn != attacker_asn):
                    # if adopting and not attacker
                    continue
                for ann_info in current_as._ribs_in.get_ann_infos(Prefixes.PREFIX.value): # noqa E501
                    if ann_info.unprocessed_ann.next_as == current_as.asn:
                        # if this ann has a signature on it, we have to process it first
                        atk_ann_candidates.append(attacker._copy_and_process(current_as._copy_and_process(ann_info.unprocessed_ann, Relationships.CUSTOMERS), Relationships.CUSTOMERS)) # noqa E501
                    else:
                        atk_ann_candidates.append(attacker._copy_and_process(ann_info.unprocessed_ann, Relationships.CUSTOMERS)) # noqa E501
                # Old code for using local RIB
                #
                #     potential_ann_to_add = current_as._local_rib.get_ann(Prefixes.PREFIX.value) # noqa E501
                #     if potential_ann_to_add is not None:
                #         atk_ann_candidates.append(attacker._copy_and_process(potential_ann_to_add, Relationships.CUSTOMERS)) # noqa E501
            for atk_ann in atk_ann_candidates:
                # Truncate path as much as possible, which is to the AS
                # after the most recent BGPsec Transitive adopter on the
                # path
                self._truncate_ann(atk_ann)

                # Clear any down only communities
                self._trim_do_communities(atk_ann)

                # Reprocess atk_ann to add the attacker's ASN
                if atk_ann.as_path[0] != attacker_asn:
                    atk_ann = attacker._copy_and_process(atk_ann, Relationships.CUSTOMERS) # noqa E501
                attack_anns.append(atk_ann)

            def bestpath(ann):
                # In BGP, paths cannot be longer than 255 because it would
                # exceed the size of the length field of the attribute
                return len(ann.as_path) + 256 * len(ann.do_communities)
            attack_anns = sorted(attack_anns, key=bestpath)
            attack_anns = attack_anns[:1]

            if len(attack_anns) == 0:
                print("Attacker did not receive announcement from victim, cannot attack") # noqa E501
                return

            self.leak_announcements_to_providers(
                attack_anns, attacker, propagation_round)

    def _truncate_ann(self, ann):
        """Truncate to the first non-adopting ASN.

        This needs to be redefined here because the attacker searches through
        RIBs_In for other ASes. This means it needs to account for the case
        where an adopting origin sends to a non-adopting neighbor which isn't
        the attacker, but also can't be removed because of the signature.
        """
        ann.as_path = ann.as_path[1:]  # remove attacker ASN
        if len(ann.as_path) == 1:
            if ann.next_as != 0:
                # announcement cannot be shortened because of origin signature
                ann.as_path = tuple([ann.next_as, ann.as_path[0]])
                ann.bgpsec_path = tuple(x for x in ann.bgpsec_path
                                        if x in ann.as_path)
                return
        partial = ann.bgpsec_path
        full = ann.as_path
        removed = ann.removed_signatures
        if len(partial) < len(removed):
            partial = removed
        i = len(partial) - 1
        j = len(full) - 1
        while (i >= 0 and j > 0 and partial[i] == full[j]):
            i -= 1
            j -= 1
        ann.as_path = ann.as_path[j:]
        # update BGPsec path to match new AS path
        ann.bgpsec_path = tuple(x for x in ann.bgpsec_path if x in ann.as_path)
