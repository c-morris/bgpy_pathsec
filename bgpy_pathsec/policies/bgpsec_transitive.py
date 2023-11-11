from copy import deepcopy
from bgpy import Relationships

from .bgpsec import BGPsecAS


class BGPsecTransitiveAS(BGPsecAS):
    name = "BGPsec Transitive"
    count = 0
    bpo_count = 0

    def _process_outgoing_ann(
        self, as_obj, ann, propagate_to, send_rels, *args, **kwargs
    ):
        ann_to_send = ann.copy()
        self.bgpsec_transitive_modifications(
            as_obj, ann_to_send, *args, **kwargs
        )
        # Although this looks weird, it is correct to call the BGPsecAS's
        # superclass here
        super(BGPsecAS, self)._process_outgoing_ann(
            as_obj, ann_to_send, propagate_to, send_rels, *args, **kwargs
        )

    def bgpsec_transitive_modifications(
        self, as_obj, ann_to_send, *args, **kwargs
    ):
        # Set next_as for bgpsec
        ann_to_send.next_as = as_obj.asn

    def _valid_ann(self, ann, recv_relationship: Relationships):
        """Determine if an announcement is valid or should be dropped"""
        BGPsecTransitiveAS.count += len(ann.bgpsec_path)
        # print(f"Added {len(ann.bgpsec_path)} at {self.asn} for total")
        # print(f"BGPsecTransitiveAS {BGPsecTransitiveAS.count}, {self.count}")
        return (
            super(BGPsecTransitiveAS, self)._valid_ann(ann, recv_relationship)
            and len(ann.removed_signatures) == 0
        )

    def _copy_and_process(
        self, ann, recv_relationship, overwrite_default_kwargs=None
    ):
        """Policy modifications to ann"""

        if overwrite_default_kwargs is None:
            overwrite_default_kwargs = dict()
        # Update the BGPsec path, but since attributes are transitive, the path
        # is always updated unlike BGPsec.
        if len(ann.bgpsec_path) == len(ann.as_path):
            overwrite_default_kwargs.update(
                {"bgpsec_path": (self.asn, *ann.bgpsec_path)}
            )

        # NOTE that after this point ann has been deep copied and processed
        # This means the AS path has 1 extra ASN that you don't need to check.
        # Although this looks weird, it is correct to call the BGPsecAS's
        # superclass here
        return super(BGPsecAS, self)._copy_and_process(
            ann, recv_relationship, overwrite_default_kwargs
        )

    def process_incoming_anns(
        self,
        *,
        from_rel: Relationships,
        propagation_round: int,
        scenario,
        reset_q: bool = True
    ):
        """Increment BPO counter when the local rib changes"""
        previous_local_rib = deepcopy(self._local_rib)
        super(BGPsecAS, self).process_incoming_anns(
            from_rel=from_rel,
            propagation_round=propagation_round,
            scenario=scenario,
            reset_q=reset_q,
        )
        for prefix, ann in self._local_rib.prefix_anns():
            if previous_local_rib.get_ann(prefix) != ann:
                BGPsecTransitiveAS.bpo_count += len(ann.bgpsec_path)

    def _partial_path_metric(self, partial, full):
        """Count the number of non-adopting segments"""
        i = 0
        j = 0
        switch = 0
        segments = 0
        if partial[0] != full[0]:
            # count first segment
            segments += 1
        while i < len(partial) and j < len(full):
            while partial[i] != full[j]:
                segments += switch
                switch = 0
                j += 1
                if j == len(full):
                    return segments
            switch = 1
            i += 1
            j += 1
        if j < len(full):
            # count last segment
            segments += 1
        return segments
