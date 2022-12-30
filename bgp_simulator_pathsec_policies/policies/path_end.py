from bgp_simulator_pkg import Relationships, BGPAS


class PathEndAS(BGPAS):

    name = "Path End"

    # These have no meaning for Path End
    # They are only here so the overhead subgraphs don't error
    count = 0
    bpo_count = 0

    __slots__ = tuple()

    def _valid_ann(self, ann, recv_relationship: Relationships):
        """Determine if an announcement is valid or should be dropped"""
        return (ann.path_end_valid and
                super(BGPAS, self)._valid_ann(ann, recv_relationship))

