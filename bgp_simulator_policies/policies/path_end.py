from bgp_simulator_pkg import Relationships

from .bgpsec import BGPsecAS


class PathEndAS(BGPsecAS):

    name = "Path End"

    __slots__ = tuple()

    def _valid_ann(self, ann, recv_relationship: Relationships):
        """Determine if an announcement is valid or should be dropped"""
        return (ann.path_end_valid and
                super(BGPsecAS, self)._valid_ann(ann, recv_relationship))
