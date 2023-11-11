from dataclasses import replace

from bgpy import BGPAS, Relationships


class DownOnlyAS(BGPAS):
    name = "Down Only"

    def _process_outgoing_ann(
        self, as_obj, ann, propagate_to, send_rels, *args, **kwargs
    ):
        ann_to_send = self.down_only_modifications(
            as_obj, ann, propagate_to, *args, **kwargs
        )
        # To make sure we don't repropagate anns we have already sent
        super(DownOnlyAS, self)._process_outgoing_ann(
            as_obj, ann_to_send, propagate_to, send_rels, *args, **kwargs
        )

    def _valid_ann(self, ann, recv_relationship: Relationships):
        """Determine if an announcement is valid or should be dropped"""
        return super(DownOnlyAS, self)._valid_ann(
            ann, recv_relationship
        ) and self.passes_down_only_checks(ann, recv_relationship)

    def down_only_modifications(
        self, as_obj, ann_to_send, propagate_to, *args, **kwargs
    ):
        # Down Only modifications, defined in section 4.2
        if propagate_to in (Relationships.CUSTOMERS, Relationships.PEERS):
            ann_to_send = replace(ann_to_send, do_communities =(
                self.asn,
                *ann_to_send.do_communities,
            ))
        return ann_to_send

    def passes_down_only_checks(self, ann, recv_relationship: Relationships):
        # Down Only Checks, defined in section 4.2
        if (
            recv_relationship == Relationships.CUSTOMERS
            and len(ann.do_communities) != 0
        ):
            return False
        if (
            recv_relationship == Relationships.PEERS
            and len(ann.do_communities) != 1
        ):
            return False
        return True
