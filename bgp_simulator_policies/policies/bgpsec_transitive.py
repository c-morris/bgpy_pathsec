from copy import deepcopy

from lib_bgp_simulator import BGPAS, LocalRIB, SendQueue, RecvQueue, Relationships

from .bgpsec import BGPsecAS

class BGPsecTransitiveAS(BGPsecAS):

    name="BGPsec Transitive"
    
    __slots__ = []

    def _process_outgoing_ann(self, as_obj, ann, propagate_to, send_rels, *args, **kwargs):
        ann_to_send = ann.copy()
        self.bgpsec_transitive_modifications(as_obj, ann_to_send, *args, **kwargs)
        # Although this looks weird, it is correct to call the BGPsecAS's
        # superclass here
        super(BGPsecAS, self)._process_outgoing_ann(as_obj, ann_to_send, propagate_to, send_rels, *args, **kwargs)

    def bgpsec_transitive_modifications(self, as_obj, ann_to_send, *args, **kwargs):
        # Set next_as for bgpsec
        ann_to_send.next_as = as_obj.asn

    def _valid_ann(self, ann, recv_relationship: Relationships):
        """Determine if an announcement is valid or should be dropped"""
        return (super(BGPsecTransitiveAS, self)._valid_ann(ann, recv_relationship) and 
                len(ann.removed_signatures) == 0)

    def _new_ann_better_bgpsec(self,
                                  current_ann,
                                  current_processed,
                                  new_ann,
                                  new_processed):
           
        # This is BGPsec Security Second, where announcements with security
        # attributes are preferred over those without, but only after
        # considering business relationships.
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
        new_ann_metric = self._partial_path_metric(new_bgpsec_path, new_path)
        current_ann_metric = self._partial_path_metric(current_bgpsec_path, current_path)
        if current_ann_metric > new_ann_metric:
            return True
        elif current_ann_metric < new_ann_metric:
            return False
        else:
            return None

    def _copy_and_process(self, ann, recv_relationship, **extra_kwargs):
        """Policy modifications to ann

        When it is decided that an annoucenemnt will be saved
        in the local RIB, first it is copied with
        copy_w_sim_attrs, then this function is called (before updated
        path) then the path is updated
        """

        # Update the BGPsec path, but since attributes are transitive, the path
        # is always updated unlike BGPsec.
        kwargs = {"bgpsec_path": (self.asn, *ann.bgpsec_path)}

        kwargs.update(extra_kwargs)
        # NOTE that after this point ann has been deep copied and processed
        # This means that the AS path has 1 extra ASN that you don't need to check
        # Although this looks weird, it is correct to call the BGPsecAS's
        # superclass here
        return super(BGPsecAS, self)._copy_and_process(ann, recv_relationship, **kwargs)

    def _partial_verify_path(self, partial, full):
        """Verify a partial path"""
        i = 0
        j = 0
        while i < len(partial) and j < len(full):
            while partial[i] != full[j]:
                j += 1
                if j == len(full):
                    return False
            i += 1
        return i == len(partial)

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
