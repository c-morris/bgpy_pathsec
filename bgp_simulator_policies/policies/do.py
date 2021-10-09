from lib_bgp_simulator import BGPRIBSPolicy, LocalRib, SendQueue, RecvQueue, Relationships

class DownOnlyPolicy(BGPRIBSPolicy):
    name = "Down Only"
    
    def _add_ann_to_q(policy_self, self, as_obj, ann, propagate_to, send_rels, *args, **kwargs):
        
        ann_to_send = ann.copy()
        policy_self.down_only_modifications(self, as_obj, ann_to_send, propagate_to, *args, **kwargs)
        # To make sure we don't repropagate anns we have already sent
        super(DownOnlyPolicy, policy_self)._add_ann_to_q(self, as_obj, ann_to_send, propagate_to, send_rels, *args, **kwargs)

    def _valid_ann(policy_self, self, ann, recv_relationship: Relationships):
        """Determine if an announcement is valid or should be dropped"""
        return (super(DownOnlyPolicy, policy_self)._valid_ann(self, ann, recv_relationship) and 
                policy_self.passes_down_only_checks(self, ann, recv_relationship))

        # BGP Loop Prevention Check
        return not (self.asn in ann.as_path)
    def down_only_modifications(policy_self, self, as_obj, ann_to_send, propagate_to, *args, **kwargs):
        # Down Only modifications, defined in section 4.2
        if propagate_to in (Relationships.CUSTOMERS, Relationships.PEERS):
            ann_to_send.do_communities = (self.asn, *ann_to_send.do_communities)

    def passes_down_only_checks(policy_self, self, ann, recv_relationship: Relationships):
        # Down Only Checks, defined in section 4.2
        if recv_relationship == Relationships.CUSTOMERS and len(ann.do_communities) != 0:
            return False
        if recv_relationship == Relationships.PEERS and len(ann.do_communities) != 1:
            return False
        return True

    #def _new_ann_is_better(policy_self,
    #                       self,
    #                       current_best_ann,
    #                       current_best_ann_processed,
    #                       new_ann,
    #                       new_ann_processed,
    #                       recv_relationship: Relationships):
    #    """Assigns the priority to an announcement according to Gao Rexford"""
    #    if not policy_self.passes_down_only_checks(self, new_ann, recv_relationship):
    #        return False
    #    return super(DownOnlyPolicy, policy_self)._new_ann_is_better(self, current_best_ann, current_best_ann_processed, new_ann, new_ann_processed, recv_relationship)
