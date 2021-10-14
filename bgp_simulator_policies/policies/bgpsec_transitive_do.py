from lib_bgp_simulator import BGPRIBsAS, LocalRib, SendQueue, RecvQueue, Relationships
from ..policies import BGPsecAS, BGPsecTransitiveAS, DownOnlyAS

class BGPsecTransitiveDownOnlyAS(BGPsecTransitiveAS, DownOnlyAS):
    # In Python, multiple inheritance resolves ambiguous attributes by looking
    # in each parent in the order that they are listed. In this case, that
    # means that attributes in the BGPsecTransitive policy take priority. 
    name = "BGPsec Transitive Down Only"
    
    def _add_ann_to_q(self, as_obj, ann, propagate_to, send_rels, *args, **kwargs):
        
        ann_to_send = ann.copy()
        self.down_only_modifications(self, as_obj, ann_to_send, propagate_to, *args, **kwargs)
        self.bgpsec_transitive_modifications(self, as_obj, ann_to_send, *args, **kwargs)
        # Although this looks weird, it is correct to call the DownOnlyAS's
        # superclass here (which is the BGPRIBsAS)
        super(DownOnlyAS, self)._add_ann_to_q(self, as_obj, ann_to_send, propagate_to, send_rels, *args, **kwargs)

