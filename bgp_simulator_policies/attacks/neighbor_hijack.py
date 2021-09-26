from lib_bgp_simulator import BGPPolicy, Attack, Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario, Graph, SimulatorEngine, DataPoint

from .. import PAnn

class NeighborHijack(Attack):
    def __init__(self, attacker=ASNs.ATTACKER.value, victim=ASNs.VICTIM.value):
        anns = [PAnn(prefix=Prefixes.PREFIX.value,
                    timestamp=Timestamps.VICTIM.value,
                    as_path=(victim,),
                    seed_asn=victim)]
        super(NeighborHijack, self).__init__(attacker, victim, anns)
        
        self.post_run_hooks = [self.hook]

    def hook(self, engine: SimulatorEngine, prev_data_point: DataPoint):
        # Add the route leak from the attacker
        attacker_ann = None
        attacker = engine.as_dict[self.attacker_asn]
        if prev_data_point.propagation_round == 0:
            attack_anns = []
            for neighbor, inner_dict in attacker.policy.ribs_in.items():
                for ann_tuple in inner_dict.values():
                    ann = ann_tuple[0]
                    atk_ann = attacker.policy._deep_copy_ann(attacker, ann, Relationships.CUSTOMERS)
                    # Truncate this ann down to a path length of 3 plus the attacker
                    if len(ann.as_path) > 4:
                        ann.as_path = ann.as_path[:1] + ann.as_path[-3:]
                    # Clear any down only communities
                    atk_ann.do_communities = tuple()
                    # This suppresses withdrawals
                    atk_ann.seed_asn = attacker.asn
                    attack_anns.append(atk_ann)

            if len(attack_anns) == 0: 
                print("Attacker did not receive announcement from victim, cannot attack")
                return
            # Send attacks to neighbors
            for neighbor in attacker.providers + attacker.peers:
                for ann in attack_anns:
                    if neighbor.asn not in ann.as_path:
                        #attacker.policy.send_q[neighbor][ann.prefix].append(ann)
                        neighbor.policy.recv_q[attacker.asn][ann.prefix].append(ann)
                        neighbor.policy.process_incoming_anns(neighbor, Relationships.CUSTOMERS)
                        # Only need to leak one announcement per neighbor
                        print("Sending Neighbor Hijack", ann, "to neighbor", neighbor.asn)
                        continue
