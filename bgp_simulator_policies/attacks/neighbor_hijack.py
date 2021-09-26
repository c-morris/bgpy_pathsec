from lib_bgp_simulator import BGPPolicy, Attack, Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario, Graph, SimulatorEngine, DataPoint

from .. import PAnn

class NeighborHijack(Attack):
    AnnCls = PAnn

    def _truncate_ann(self, ann):
        # Truncate this ann down to a path length of 3 plus the attacker
        if len(ann.as_path) > 4:
            ann.as_path = ann.as_path[:1] + ann.as_path[-3:]
