from copy import deepcopy

from lib_bgp_simulator import BGPRIBSPolicy, LocalRib, RibsIn, RibsOut, SendQueue, RecvQueue, Relationships

from .bgpsec import BGPsecPolicy

class BGPsecTransitivePolicy(BGPsecPolicy):

    name="BGPsec Transitive"

    def _new_ann_is_better(policy_self, self, deep_ann, shallow_ann, recv_relationship: Relationships):
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
        """Deep copies ann and modifies attrs"""

        kwargs = dict()
        # Put default kwargs here
        kwargs.update(extra_kwargs)

        return super(BGPsecTransitivePolicy, policy_self)._deep_copy_ann(self, ann, recv_relationship, **kwargs)

    def _partial_verify_path(policy_self, partial, full):
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
