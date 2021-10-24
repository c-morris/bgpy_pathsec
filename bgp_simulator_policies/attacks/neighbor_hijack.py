from lib_bgp_simulator import Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario, Graph, SimulatorEngine, DataPoint

from .mh_path_manipulation import MHPathManipulation
from .. import PAnn

class NeighborHijack(MHPathManipulation):

    def _truncate_ann(self, ann):
        # Truncate this ann down to a path length of 3 plus the attacker
        if len(ann.as_path) > 4:
            ann.as_path = ann.as_path[:1] + ann.as_path[-3:]
