
from copy import deepcopy

from lib_bgp_simulator import BGPRIBSPolicy, LocalRib, RibsIn, RibsOut, SendQueue, RecvQueue, Relationships

class DownOnlyPolicy(BGPRIBSPolicy):
    name = "Down Only"
    
    def _populate_send_q(policy_self, self, propagate_to, send_rels):
        """Populates send queue"""

        for as_obj in getattr(self, propagate_to.name.lower()):
            for prefix, ann in policy_self.local_rib.items():
                if ann.recv_relationship in send_rels:
                    ann_to_send = deepcopy(ann)
                    # Down Only Community
                    if propagate_to == Relationships.CUSTOMERS:
                        ann_to_send.do_communities = (self.asn, *(ann_to_send.do_communities))
                    ribs_out_ann = policy_self.ribs_out[as_obj.asn].get(prefix)
                    # To make sure we don't repropagate anns we have already sent
                    if not ann.prefix_path_attributes_eq(ribs_out_ann):
                        policy_self.send_q[as_obj.asn][prefix].append(ann_to_send)

    def _new_ann_is_better(policy_self, self, deep_ann, shallow_ann, recv_relationship: Relationships):
        """Assigns the priority to an announcement according to Gao Rexford"""
        
        # Down Only Check
        if recv_relationship == Relationships.CUSTOMERS and len(shallow_ann.do_communities) != 0:
            return False

        return super(DownOnlyPolicy, policy_self)._new_ann_is_better(self, deep_ann, shallow_ann, recv_relationship)
