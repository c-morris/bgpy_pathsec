from bgp_simulator_pkg import Prefixes, Relationships

from .mh_leak import MHLeak


class IntentionalLeak(MHLeak):
    """Intentional, but timid route leak.

    The attack is "timid" in that the attacker will only modify the AS path in
    ways that will not be detected by PaBGPsec.

    The attack is intentional in that the attacker will attempt to shorten the
    AS path as much as possible, removing BGPsec signatures and Down-Only
    communities in the process. The attacker will also choose the optimal
    announcement to leak to each provider to maximize the effectiveness of the
    attack. This means, for multi-homed attackers, when the path cannot be
    shortened, no provider will receive the same announcement that they sent to
    the attacker (so the announcements are not rejected for having the
    provider's ASN on them).
    """

    def __init__(self, no_hash=True, communities_up=True, unknown_adopter=False, **kwargs):
        super().__init__(**kwargs)
        self.no_hash = no_hash
        self.communities_up = communities_up
        self.unknown_adopter = unknown_adopter

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
            for ann_info in attacker._ribs_in.get_ann_infos(Prefixes.PREFIX.value): # noqa E501
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

            def pathlen(ann):
                return len(ann.as_path)
            attack_anns = sorted(attack_anns, key=pathlen)

            if len(attack_anns) == 0:
                print("Attacker did not receive announcement from victim, cannot attack") # noqa E501
                return

            self.leak_announcements_to_providers(
                attack_anns, attacker, propagation_round)

    def leak_announcements_to_providers(self,
                                        attack_anns,
                                        attacker,
                                        propagation_round):
        for neighbor in attacker.providers:
            # Populate neighbor recv_q with leaks
            current_best_ann = None
            current_best_ann_processed = True
            for ann in attack_anns:
                if neighbor.asn not in ann.as_path:
                    new_ann_is_better = False
                    recv_relationship = Relationships.CUSTOMERS
                    if current_best_ann is not None:
                        new_ann_is_better = attacker._new_ann_better(
                            current_best_ann,
                            current_best_ann_processed,
                            recv_relationship,
                            ann,
                            True,
                            recv_relationship)
                    # If the new priority is higher
                    if new_ann_is_better or current_best_ann is None:
                        current_best_ann = ann
                        current_best_ann_processed = True

            if current_best_ann is not None:
                # Only need to leak one announcement per neighbor
                neighbor._recv_q.add_ann(current_best_ann)
                neighbor.process_incoming_anns(from_rel=Relationships.CUSTOMERS, # noqa E501
                                               propagation_round=propagation_round, # noqa E501
                                               scenario=self)

    def _truncate_ann(self, ann):
        if self.unknown_adopter:
            self._truncate_ann_unknown_adopter(ann)
        elif self.no_hash:
            self._truncate_ann_no_hash(ann)
        else:
            self._truncate_ann_hash(ann)

    def _truncate_ann_hash(self, ann):
        """

        This must tuncate to two cases: either the last adopting AS on the path
        is replaced by the attacker (case 2) or the path is truncated to one
        after the last sequence of two or more adopting ASes (or the origin)
        (case 1). To generate the final attack path, we attempt to find both
        cases and choose the longer one.

        Case 1:
          bgpsec_path:         [y, z]
              as_path: [666, x, y, z]
             atk_path: [666, x, y, z]

        Case 2:
          bgpsec_path:      [x, z]
              as_path: [666, x, y, z]
             atk_path: [666, y, z]

        The announcement will be reprocessed after, so the attacker's ASN will
        be re-added to the AS path.
        """
        ann.as_path = ann.as_path[1:]  # remove attacker ASN
        # Case 0: if path is un-truncatable
        if (len(ann.as_path) < 2 or
            (len(ann.bgpsec_path) > 1 and
             ann.as_path[0] == ann.bgpsec_path[0] and
             ann.as_path[1] == ann.bgpsec_path[1]) or
            len(ann.as_path) == len(ann.bgpsec_path)): # noqa E129

            # Return without modifying path
            return

        # Case 1
        i = 0  # bgpsec path
        j = 0  # as path
        case1path = []
        while i < len(ann.bgpsec_path) and j+1 < len(ann.as_path):
            while (ann.bgpsec_path[i] != ann.as_path[j] and
                   j+1 < len(ann.as_path)):
                j += 1
            if (j > 0 and
                i+1 < len(ann.bgpsec_path) and
                (j+1 == len(ann.as_path) or
                 ann.bgpsec_path[i+1] == ann.as_path[j+1])):
                case1path = ann.as_path[j-1:]
                break
            i += 1

        # Case 2
        i = 0  # bgpsec path
        j = 0  # as path
        case2path = []
        while i < len(ann.bgpsec_path) and j+1 < len(ann.as_path):
            while (ann.bgpsec_path[i] != ann.as_path[j] and
                   j+1 < len(ann.as_path)):
                j += 1
            if ann.bgpsec_path[i] == ann.as_path[j]:
                if j+1 == len(ann.as_path):
                    case2path = ann.as_path[j-1:]
                    break
                else:
                    # replace last adopting
                    case2path = ann.as_path[j+1:]
                    break
            i += 1

        if case1path == [] and case2path == []:
            return
        if len(case1path) > len(case2path):
            ann.as_path = case1path
        else:
            ann.as_path = case2path
        ann.bgpsec_path = tuple(x for x in ann.bgpsec_path if x in ann.as_path)

        # Set the path_end attribute
        if len(ann.as_path) < 2:
            ann.path_end_valid = False

    def _truncate_ann_no_hash(self, ann):
        """Truncate to the first non-adopting ASN."""
        ann.as_path = ann.as_path[1:]  # remove attacker ASN
        partial = ann.bgpsec_path
        full = ann.as_path
        removed = ann.removed_signatures
        if len(partial) < len(removed):
            partial = removed
        i = len(partial) - 1
        j = len(full) - 1
        while i >= 0 and j > 0 and partial[i] == full[j]:
            i -= 1
            j -= 1
        ann.as_path = ann.as_path[j:]
        # update BGPsec path to match new AS path
        ann.bgpsec_path = tuple(x for x in ann.bgpsec_path if x in ann.as_path)

    def _truncate_ann_unknown_adopter(self, ann):
        old_bgpsec_path = ann.bgpsec_path
        ann.bgpsec_path = tuple()

        for _asn in old_bgpsec_path:
            if _asn not in ann.unknown_adopters:
                ann.bgpsec_path += (_asn,)

        self._truncate_ann_no_hash(ann)

    def _trim_do_communities(self, ann):
        if self.communities_up:
            self._trim_do_communities_up(ann)
        else:
            self._trim_do_communities_down(ann)

    def _trim_do_communities_down(self, ann):
        ann.do_communities = tuple(x for x in ann.do_communities
                                   if x in ann.bgpsec_path)
        
    def _trim_do_communities_up(self, ann):
        """With UP attributes, no DO communities are removed.

        The reasoning for this is as follows:
        Since the origin is always adopting, there is always at least one UP
        attribute on the announcement. If any down-only communities are also
        present, it means the UP preimage was also removed, and any leaks
        will be detected. Therefore, if any down-only communities are
        present, they should not be removed.
        """
        ann.up_pre = False
