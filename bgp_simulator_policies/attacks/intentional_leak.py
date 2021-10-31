from lib_bgp_simulator import Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario, Graph, SimulatorEngine, DataPoint, ROAValidity

from .mh_leak import MHLeak
from .. import PAnn

class IntentionalLeak(MHLeak):
    def post_propagation_hook(self, engine: SimulatorEngine, prev_data_point: DataPoint, *args, **kwargs):
        # check attacker properties...
        for i, rank in enumerate(engine.propagation_ranks):
            for as_obj in rank:
                if as_obj.asn == self.attacker_asn:
                    if i != 0:
                        print("ATTACKER RANK WAS", i)
                        exit(i)
        # Add the route leak from the attacker
        attacker_ann = None
        attacker = engine.as_dict[self.attacker_asn]
# debug
        if len(attacker.customers) != 0:
            input("WHAT IS GOING ON THE ATTACKER HAS CUSTOMERS", self.attacker_asn, len(attacker.customers))
        if prev_data_point.propagation_round == 0:
            attack_anns = []
            for ann_info in attacker._ribs_in.get_ann_infos(Prefixes.PREFIX.value):
                atk_ann = attacker._copy_and_process(ann_info.unprocessed_ann, Relationships.CUSTOMERS)
                # Truncate path as much as possible, which is to the AS
                # after the most recent BGPsec Transitive adopter on the
                # path
                self._truncate_ann(atk_ann)

                # Clear any down only communities
                atk_ann.do_communities = tuple()
                
                # Reprocess atk_ann to add the attacker's ASN
                atk_ann = attacker._copy_and_process(atk_ann, Relationships.CUSTOMERS)
                attack_anns.append(atk_ann)

            if len(attack_anns) == 0: 
                print("Attacker did not receive announcement from victim, cannot attack")
                return
            # Populate neighbor recv_q with leaks
            for neighbor in attacker.providers + attacker.peers:
                current_best_ann = None
                for ann in attack_anns:
                    if neighbor.asn not in ann.as_path:
                        new_ann_is_better = False
                        recv_relationship = Relationships.CUSTOMERS
                        if current_best_ann is not None:
                            new_ann_is_better = attacker._new_ann_better(current_best_ann,
                                                                         current_best_ann_processed,
                                                                         recv_relationship,
                                                                         ann,
                                                                         False,
                                                                         recv_relationship)
                        # If the new priority is higher
                        if new_ann_is_better or current_best_ann is None:
                            current_best_ann = ann
                            current_best_ann_processed = False

                #attacker.policy.send_q[neighbor][ann.prefix].append(ann)
                if current_best_ann is not None:
                    # Only need to leak one announcement per neighbor
                    print("Attacker", self.attacker_asn, "Leaking", ann, "to neighbor", neighbor.asn)
                    neighbor._recv_q.add_ann(ann)
                    neighbor.process_incoming_anns(Relationships.CUSTOMERS)

    @staticmethod
    def _truncate_ann(ann):
        j = 0
        while ann.bgpsec_path[0] != ann.as_path[j]:
            j += 1
        if j == 0: # cannot truncate
            return
        # Decrement j to get one after the most recent adopting AS
        ann.as_path = ann.as_path[j-1:]

    @staticmethod
    def _trim_do_communities(ann):
        ann.do_communities = tuple(x for x in ann.do_communities if x in ann.bgpsec_path)
