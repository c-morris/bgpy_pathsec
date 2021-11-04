from lib_bgp_simulator import Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario, Graph, SimulatorEngine, DataPoint, ROAValidity

from .mh_leak import MHLeak
from .intentional_leak import IntentionalLeak
from .. import PAnn

class IntentionalLeakNoHash(IntentionalLeak):

    @staticmethod
    def _truncate_ann(ann):
        partial = ann.bgpsec_path
        full = ann.as_path
        i = len(partial) - 1
        j = len(full) - 1
        while partial[i] == full[j] and i >= 0 and j > 0:
            i -= 1
            j -= 1
        ann.as_path = ann.as_path[j:]

