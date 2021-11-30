from lib_bgp_simulator import SendQueue, RecvQueue, Relationships
from ..policies import BGPsecAS, BGPsecTransitiveAS, DownOnlyAS

class BGPsecTransitiveDownOnlyAS(BGPsecTransitiveAS, DownOnlyAS):
    # In Python, multiple inheritance resolves ambiguous attributes by looking
    # in each parent in the order that they are listed. In this case, that
    # means that attributes in the BGPsecTransitive policy take priority. 
    name = "BGPsec Transitive Down Only"
    
    __slots__ = tuple()
    
    def _process_outgoing_ann(self, as_obj, ann, propagate_to, send_rels, *args, **kwargs):

        ann_to_send = ann.copy()
        self.down_only_modifications(as_obj, ann_to_send, propagate_to, send_rels, *args, **kwargs)
        self.bgpsec_transitive_modifications(as_obj, ann_to_send, propagate_to, send_rels, *args, **kwargs)
        # Although this looks weird, it is correct to call the DownOnlyAS's
        # superclass here (which is the BGPAS)
        super(DownOnlyAS, self)._process_outgoing_ann(as_obj, ann_to_send, propagate_to, send_rels, *args, **kwargs)
