from copy import deepcopy

from lib_bgp_simulator import BGPRIBsAS, LocalRib, SendQueue, RecvQueue, Relationships

class BGPsecAS(BGPRIBsAS):

    name="BGPsec"

    def _add_ann_to_q(self, as_obj, ann, *args):

        # Set next_as for bgpsec
        next_as = as_obj.asn if ann.next_as == self.asn else ann.next_as

        super(BGPsecAS, self)._add_ann_to_q(
                                                     as_obj,
                                                     ann.copy(next_as=next_as), *args)
    def _new_ann_is_better(self,
                           current_ann,
                           current_processed,
                           default_current_recv_rel,
                           new_ann,
                           new_processed,
                           default_new_recv_rel):
        """Assigns the priority to an announcement according to Gao Rexford

        NOTE: processed is processed for second ann"""

        # Can't assert this here due to passing new_ann as None now that it can be prpcessed or not
        #assert self.asn not in new_ann.as_path, "Should have been removed in ann validation func"

        new_rel_better = self._new_rel_better(current_ann,
                                                     current_processed,
                                                     default_current_recv_rel,
                                                     new_ann,
                                                     new_processed,
                                                     default_new_recv_rel)
        if new_rel_better is not None:
            return new_rel_better
        else:
            bgpsec_better = self._new_ann_is_better_bgpsec(
                                                           current_ann,
                                                           current_processed,
                                                           new_ann,
                                                           new_processed)
            if (bgpsec_better is not None):
                return  bgpsec_better
            else:
                new_as_path_shorter = self._new_as_path_shorter(current_ann,
                                                                current_processed,
                                                                new_ann,
                                                                new_processed)
                if new_as_path_shorter is not None:
                    return new_as_path_shorter
                else:
                    return self._new_wins_ties(current_ann,
                                               current_processed,
                                               new_ann,
                                               new_processed)


    def _new_ann_is_better_bgpsec(self,
                                  current_ann,
                                  current_processed,
                                  new_ann,
                                  new_processed):
        # This is BGPsec Security Second, where announcements with security
        # attributes are preferred over those without, but only after
        # considering business relationships.
        current_ann_valid = current_ann.bgpsec_path == current_ann.as_path and current_ann.next_as == self.asn
        new_ann_valid = new_ann.bgpsec_path == new_ann.as_path and new_ann.next_as == self.asn
        if new_ann_valid and not current_ann_valid:
            return True
        elif current_ann_valid and not new_ann_valid:
            return False
        else:
            return None

    def _deep_copy_ann(self, ann, recv_relationship, **extra_kwargs):
        """Policy modifications to ann

        When it is decided that an annoucenemnt will be saved
        in the local RIB, first it is copied with
        copy_w_sim_attrs, then this function is called (before updated
        path) then the path is updated
        """

        # Update the BGPsec path, too
        if ann.bgpsec_path == ann.as_path:
            # If paths are equal, there is an unbroken chain of adopters,
            # otherwise, the attributes are lost
            kwargs = {"bgpsec_path": (self.asn, *ann.bgpsec_path)}
        else:
            kwargs = {"bgpsec_path": tuple(), "next_as": 0}

        kwargs.update(extra_kwargs)
        # NOTE that after this point ann has been deep copied and processed
        # This means that the AS path has 1 extra ASN that you don't need to check
        return super(BGPsecAS, self)._deep_copy_ann(self, ann, recv_relationship, **kwargs)
