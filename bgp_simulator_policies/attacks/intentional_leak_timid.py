from lib_bgp_simulator import Prefixes, Relationships

from .intentional_leak import IntentionalLeak


class IntentionalLeakTimid(IntentionalLeak):
    """Same as IntentionalLeak, but timid.

    It will only leak if it can leak an announcement with no DO communities.
    """

    def post_propagation_hook(self, engine,
                              prev_data_point, *args, **kwargs):
        """Add the route leak from the attacker"""
        attacker_ann = None
        # Freeze this current ann in the local rib of the attacker
        attacker_ann = engine.as_dict[self.attacker_asn]._local_rib.get_ann(Prefixes.PREFIX.value) # noqa E501
        if attacker_ann is not None:
            attacker_ann.seed_asn = self.attacker_asn
        attacker = engine.as_dict[self.attacker_asn]
        if prev_data_point.propagation_round == 0:
            attack_anns = []
            for ann_info in attacker._ribs_in.get_ann_infos(Prefixes.PREFIX.value): # noqa E501
                atk_ann = attacker._copy_and_process(ann_info.unprocessed_ann, Relationships.CUSTOMERS) # noqa E501
                # Truncate path as much as possible, which is to the AS
                # after the most recent BGPsec Transitive adopter on the
                # path
                #print('pre truncated', atk_ann)
                #print('apath', atk_ann.as_path)
                #print('bpath', atk_ann.bgpsec_path)
                prev_len = len(atk_ann.as_path)
                self._truncate_ann(atk_ann)

                #print('truncated', atk_ann)
                # Clear any down only communities
                self._trim_do_communities(atk_ann)
                if len(atk_ann.do_communities) > 0:
                    # If there are any DO communities, this is un-leakable
                    #print('Skipping Leak', atk_ann)
                    continue

                # Reprocess atk_ann to add the attacker's ASN
                if prev_len != len(atk_ann.as_path):
                    atk_ann = attacker._copy_and_process(atk_ann, Relationships.CUSTOMERS) # noqa E501
                attack_anns.append(atk_ann)

            if len(attack_anns) == 0:
                print("Attacker did not receive announcement from victim, cannot attack") # noqa E501
                return
            # Populate neighbor recv_q with leaks
            for neighbor in attacker.providers:
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
                    neighbor.process_incoming_anns(Relationships.CUSTOMERS)

