from lib_bgp_simulator import Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario, Graph, SimulatorEngine, DataPoint, ROAValidity

from .mh_leak import MHLeak
from .. import PAnn

#(666, 666, 5, 4, 1, 7, 10, 13, 777)

# TIMID

class IntentionalLeak(MHLeak):
    def post_propagation_hook(self, engine: SimulatorEngine, prev_data_point: DataPoint, *args, **kwargs):
        # Add the route leak from the attacker
        attacker_ann = None
        # Freeze this current ann in the local rib of the attacker
        attacker_ann = engine.as_dict[self.attacker_asn]._local_rib.get_ann(Prefixes.PREFIX.value)
        if attacker_ann is not None:
            attacker_ann.seed_asn = self.attacker_asn
        attacker = engine.as_dict[self.attacker_asn]
        if prev_data_point.propagation_round == 0:
            attack_anns = []
            for ann_info in attacker._ribs_in.get_ann_infos(Prefixes.PREFIX.value):
                atk_ann = attacker._copy_and_process(ann_info.unprocessed_ann, Relationships.CUSTOMERS)
                # Truncate path as much as possible, which is to the AS
                # after the most recent BGPsec Transitive adopter on the
                # path
                prev_len = len(atk_ann.as_path)
                self._truncate_ann(atk_ann)

                # Clear any down only communities
                self._trim_do_communities(atk_ann)
                
                # Reprocess atk_ann to add the attacker's ASN
                if prev_len != len(atk_ann.as_path):
                    atk_ann = attacker._copy_and_process(atk_ann, Relationships.CUSTOMERS)
                attack_anns.append(atk_ann)

            if len(attack_anns) == 0: 
                print("Attacker did not receive announcement from victim, cannot attack")
                return
            # Populate neighbor recv_q with leaks
            for neighbor in attacker.providers:
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
                                                                         True,
                                                                         recv_relationship)
                        # If the new priority is higher
                        if new_ann_is_better or current_best_ann is None:
                            current_best_ann = ann
                            current_best_ann_processed = True

                #attacker.policy.send_q[neighbor][ann.prefix].append(ann)
                if current_best_ann is not None:
                    # Only need to leak one announcement per neighbor
                    print("Attacker", self.attacker_asn, "Leaking", current_best_ann, "to neighbor", neighbor.asn)
                    neighbor._recv_q.add_ann(current_best_ann)
                    neighbor.process_incoming_anns(Relationships.CUSTOMERS)

    #@staticmethod
    #def _truncate_ann(ann):
    #    j = 0
    #    while ann.bgpsec_path[0] != ann.as_path[j]:
    #        j += 1
    #    if j == 0: # cannot truncate
    #        return
    #    # Decrement j to get one after the most recent adopting AS
    #    ann.as_path = ann.as_path[j-1:]

    @staticmethod
    def _truncate_ann(ann):
        """

        This must tuncate to two cases: either the last adopting AS on the path
        is replaced by the attacker or the path is truncated to one after the
        last sequence of two or more adopting ASes (or the origin). To generate
        the final attack path, we attempt to find both cases and choose the
        shorter one.

        Case 1: 
          bgpsec_path:         [y, z]
              as_path:      [x, y, z]
             atk_path: [666, x, y, z]

        Case 2: 
          bgpsec_path: [x, z]
              as_path: [x, y, z]
             atk_path: [666, y, z]
        """
        # Case 0: if path is un-truncatable
        if len(ann.as_path) < 2 or len(ann.as_path) == len(ann.bgpsec_path):
            # Return without modifying path
            return 

        # Case 1
        i = 0 # bgpsec path
        j = 0 # as path
        case1path = ann.as_path
        while i < len(ann.bgpsec_path) and j+1 < len(ann.as_path):
            while ann.bgpsec_path[i] != ann.as_path[j] and j+1 < len(ann.as_path):
                j += 1
            if j > 0 and ann.bgpsec_path[i] == ann.as_path[j-1] and (ann.bgpsec_path[i+1] == ann.as_path[j+1] or j+1 == len(ann.as_path)):
                case1path = ann.as_path[j-1:]
            i += 1
        
        # Case 2
        i = 0 # bgpsec path
        j = 0 # as path
        case2path = ann.as_path
        while i < len(ann.bgpsec_path) and j+1 < len(ann.as_path):
            while ann.bgpsec_path[i] != ann.as_path[j] and j+1 < len(ann.as_path):
                j += 1
            if ann.bgpsec_path[i] == ann.as_path[j]:
                if j+1 == len(ann.as_path):
                    case2path = ann.as_path[j-1:]
                    break
                if ann.bgpsec_path[i+1] != ann.as_path[j+1]:
                    # found one
                    case2path = ann.as_path[j:]
                    break
            i += 1

        if len(case1path) < len(case2path):
            ann.as_path = case1path
        else:
            ann.as_path = case2path

    @staticmethod
    def _trim_do_communities(ann):
        ann.do_communities = tuple(x for x in ann.do_communities if x in ann.bgpsec_path)
