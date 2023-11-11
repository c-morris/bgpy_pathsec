from bgpy import Relationships

from ..policies import BGPsecTransitiveAS, DownOnlyAS


class BGPsecTransitiveDownOnlyAS(BGPsecTransitiveAS, DownOnlyAS):
    # In Python, multiple inheritance resolves ambiguous attributes by looking
    # in each parent in the order that they are listed. In this case, that
    # means that attributes in the BGPsecTransitive policy take priority.
    name = "BGPsec Transitive Down Only"

    def _valid_ann(self, ann, recv_relationship: Relationships):
        """Determine if an announcement is valid or should be dropped"""
        BGPsecTransitiveAS.count += len(ann.bgpsec_path)
        return (
            super(BGPsecTransitiveAS, self)._valid_ann(ann, recv_relationship)
            and self.passes_down_only_checks(
                ann, recv_relationship
            )
            and len(ann.removed_signatures) == 0
        )

    def _process_outgoing_ann(
        self, as_obj, ann, propagate_to, send_rels, *args, **kwargs
    ):
        ann_to_send = self.down_only_modifications(
            as_obj, ann, propagate_to, send_rels, *args, **kwargs
        )
        ann_to_send = self.bgpsec_transitive_modifications(
            as_obj, ann_to_send, propagate_to, send_rels, *args, **kwargs
        )
        # Although this looks weird, it is correct to call the DownOnlyAS's
        # superclass here (which is the BGPAS)
        super(DownOnlyAS, self)._process_outgoing_ann(
            as_obj, ann_to_send, propagate_to, send_rels, *args, **kwargs
        )
