from bgp_simulator_pkg import Prefixes, Relationships

from .shortest_path_export_all_no_hash import ShortestPathExportAllNoHash


class Eavesdropper(ShortestPathExportAllNoHash):
    """Attacker has visibility into other AS RIBs.
       Vantage points must be defined in subclasses.
    """

    vantage_points = []

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
            for asn in [attacker_asn] + self.vantage_points:
                current_as = engine.as_dict[asn]
                for ann_info in current_as._ribs_in.get_ann_infos(Prefixes.PREFIX.value): # noqa E501
                    atk_ann = attacker._copy_and_process(ann_info.unprocessed_ann, Relationships.CUSTOMERS) # noqa E501
                    # Truncate path as much as possible, which is to the AS
                    # after the most recent BGPsec Transitive adopter on the
                    # path
                    prev_len = len(atk_ann.as_path)
                    self._truncate_ann(atk_ann)

                    # Clear any down only communities
                    self._trim_do_communities(atk_ann)

                    # Reprocess atk_ann to add the attacker's ASN
                    if prev_len != len(atk_ann.as_path):
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
