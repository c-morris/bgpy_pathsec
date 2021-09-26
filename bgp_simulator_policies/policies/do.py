
from copy import deepcopy

from lib_bgp_simulator import BGPRIBSPolicy, LocalRib, RibsIn, RibsOut, SendQueue, RecvQueue, Relationships

class DownOnlyPolicy(BGPRIBSPolicy):
    name = "Down Only"
    
    def _add_ann_to_send_q(policy_self, self, as_obj, ann, propagate_to, *args):
        
        ann_to_send = ann.copy()
        # Down Only Community
        if propagate_to == Relationships.CUSTOMERS:
            ann_to_send.do_communities = (self.asn, *ann_to_send.do_communities)
        # To make sure we don't repropagate anns we have already sent
        super(DownOnlyPolicy, policy_self)._add_ann_to_send_q(self, as_obj, ann_to_send, propagate_to, *args)

    def _new_ann_is_better(policy_self, self, deep_ann, shallow_ann, recv_relationship: Relationships):
        """Assigns the priority to an announcement according to Gao Rexford"""
        
        # Down Only Check
        if recv_relationship == Relationships.CUSTOMERS and len(shallow_ann.do_communities) != 0:
            return False

        return super(DownOnlyPolicy, policy_self)._new_ann_is_better(self, deep_ann, shallow_ann, recv_relationship)
