from lib_bgp_simulator import BGPRIBsAS, LocalRib, SendQueue, RecvQueue, Relationships

class DownOnlyAS(BGPRIBsAS):
    name = "Down Only"
    
    def _add_ann_to_q(self, as_obj, ann, propagate_to, send_rels, *args, **kwargs):
        
        ann_to_send = ann.copy()
        self.down_only_modifications(as_obj, ann_to_send, propagate_to, *args, **kwargs)
        # To make sure we don't repropagate anns we have already sent
        super(DownOnlyAS, self)._add_ann_to_q(as_obj, ann_to_send, propagate_to, send_rels, *args, **kwargs)

    def _valid_ann(self, ann, recv_relationship: Relationships):
        """Determine if an announcement is valid or should be dropped"""
        return (super(DownOnlyAS, self)._valid_ann(ann, recv_relationship) and 
                self.passes_down_only_checks(ann, recv_relationship))

        # BGP Loop Prevention Check
        return not (self.asn in ann.as_path)
    def down_only_modifications(self, as_obj, ann_to_send, propagate_to, *args, **kwargs):
        # Down Only modifications, defined in section 4.2
        if propagate_to in (Relationships.CUSTOMERS, Relationships.PEERS):
            ann_to_send.do_communities = (self.asn, *ann_to_send.do_communities)

    def passes_down_only_checks(self, ann, recv_relationship: Relationships):
        # Down Only Checks, defined in section 4.2
        if recv_relationship == Relationships.CUSTOMERS and len(ann.do_communities) != 0:
            return False
        if recv_relationship == Relationships.PEERS and len(ann.do_communities) != 1:
            return False
        return True
