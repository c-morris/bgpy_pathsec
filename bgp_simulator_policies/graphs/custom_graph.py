import random

from lib_bgp_simulator import BGPPolicy, Attack, Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario, Graph

class CustomGraph(Graph):
    from .custom_writer import aggregate_and_write
    from .custom_writer import _write

