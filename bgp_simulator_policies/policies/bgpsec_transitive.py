from bgp_simulator_pkg import Relationships

from .bgpsec import BGPsecAS


class BGPsecTransitiveAS(BGPsecAS):

    name = "BGPsec Transitive"

    __slots__ = []

    def _process_outgoing_ann(self, as_obj, ann, propagate_to, send_rels, *args, **kwargs): # noqa E501
        ann_to_send = ann.copy()
        self.bgpsec_transitive_modifications(as_obj, ann_to_send, *args,
                                             **kwargs)
        # Although this looks weird, it is correct to call the BGPsecAS's
        # superclass here
        super(BGPsecAS, self)._process_outgoing_ann(as_obj,
                                                    ann_to_send,
                                                    propagate_to,
                                                    send_rels,
                                                    *args,
                                                    **kwargs)

    def bgpsec_transitive_modifications(self, as_obj, ann_to_send, *args, **kwargs): # noqa E501
        # Set next_as for bgpsec
        ann_to_send.next_as = as_obj.asn

    def _valid_ann(self, ann, recv_relationship: Relationships):
        """Determine if an announcement is valid or should be dropped"""
        return (super(BGPsecTransitiveAS, self)._valid_ann(ann, recv_relationship) and  # noqa E501
                len(ann.removed_signatures) == 0)

    def _old_new_ann_better_bgpsec(self,
                                   current_ann,
                                   current_processed,
                                   new_ann,
                                   new_processed):

        # This is BGPsec Security Third, where announcements with full security
        # attributes are preferred over those without, but only after
        # considering path length.

        # Need to get the paths without the current ASN so they are comparable
        if current_processed:
            current_path = current_ann.as_path[1:]
            current_bgpsec_path = current_ann.bgpsec_path[1:]
        else:
            current_path = current_ann.as_path
            current_bgpsec_path = current_ann.bgpsec_path
        if new_processed:
            new_path = new_ann.as_path[1:]
            new_bgpsec_path = new_ann.bgpsec_path[1:]
        else:
            new_path = new_ann.as_path
            new_bgpsec_path = new_ann.bgpsec_path

        current_ann_valid = current_bgpsec_path == current_path and current_ann.next_as == self.asn # noqa E501
        new_ann_valid = new_bgpsec_path == new_path and new_ann.next_as == self.asn # noqa E501
        # Old metric code may become relevant again if using bloom filter
        # new_ann_metric = self._partial_path_metric(new_bgpsec_path, new_path)
        # current_ann_metric = self._partial_path_metric(current_bgpsec_path,
        #                                                current_path)

        # Do not give preference to partly signed paths
        if new_ann_valid and not current_ann_valid:
            return True
        elif current_ann_valid and not new_ann_valid:
            return False
        else:
            return None

    def _copy_and_process(self,
                          ann,
                          recv_relationship,
                          overwrite_default_kwargs=None):
        """Policy modifications to ann"""

        if overwrite_default_kwargs is None:
            overwrite_default_kwargs = dict()
        # Update the BGPsec path, but since attributes are transitive, the path
        # is always updated unlike BGPsec.
        overwrite_default_kwargs.update({"bgpsec_path": (self.asn, *ann.bgpsec_path)}) # noqa E501

        # NOTE that after this point ann has been deep copied and processed
        # This means the AS path has 1 extra ASN that you don't need to check.
        # Although this looks weird, it is correct to call the BGPsecAS's
        # superclass here
        return super(BGPsecAS, self)._copy_and_process(ann, recv_relationship,
                                                       overwrite_default_kwargs) # noqa E501

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
