from copy import deepcopy

from lib_bgp_simulator import BGPRIBSPolicy, LocalRib, RibsIn, RibsOut, SendQueue, RecvQueue, Relationships

class BGPsecPolicy(BGPRIBSPolicy):

    name="BGPsec"

    def _add_ann_to_q(policy_self, self, as_obj, ann, *args):

        # Set next_as for bgpsec
        next_as = as_obj.asn if ann.next_as == self.asn else ann.next_as

        super(BGPsecPolicy, policy_self)._add_ann_to_q(self,
                                                     as_obj,
                                                     ann.copy(next_as=next_as), *args)

    def _new_ann_is_better(policy_self, self, deep_ann, shallow_ann, recv_relationship: Relationships, *args):
        """Assigns the priority to an announcement according to Gao Rexford"""

        if deep_ann is None:
            return True

        if deep_ann.recv_relationship.value > recv_relationship.value:
            return False
        elif deep_ann.recv_relationship.value < recv_relationship.value:
            return True
        else:
            # This is BGPsec Security Second, where announcements with security
            # attributes are preferred over those without, but only after
            # considering business relationships.
            deep_ann_valid = deep_ann.bgpsec_path == deep_ann.as_path and deep_ann.next_as == self.asn
            shallow_ann_valid = shallow_ann.bgpsec_path == shallow_ann.as_path and shallow_ann.next_as == self.asn
            if shallow_ann_valid and not deep_ann_valid:
                return True
            if len(deep_ann.as_path) < len(shallow_ann.as_path) + 1:
                return False
            elif len(deep_ann.as_path) > len(shallow_ann.as_path) + 1:
                return True
            else:
                return not deep_ann.as_path[0] <= self.asn

    def _deep_copy_ann(policy_self, self, ann, recv_relationship, **extra_kwargs):
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
        return super(BGPsecPolicy, policy_self)._deep_copy_ann(self, ann, recv_relationship, **kwargs)
