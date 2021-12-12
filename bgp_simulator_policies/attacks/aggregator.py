from lib_bgp_simulator import Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario, Graph, SimulatorEngine, DataPoint, ROAValidity

from .mh_path_manipulation import MHPathManipulation
from . import OriginHijack, IntentionalLeak, IntentionalLeakNoHash

# This is an aggregation of attacks and policies
# this *only* works with a specific set of policies!
# any deviation may produce unexpected results

class Aggregator(MHPathManipulation):
    counter = 0
    # The order of the attack classes must correspond with the policies in the run script!
    AttackClses = [OriginHijack, OriginHijack, OriginHijack, OriginHijack, IntentionalLeak, IntentionalLeak, IntentionalLeakNoHash]
    # policies: [BGP, BGPsecAggressive, BGPsecTransitiveAggressive, 
    #            BGPsecTransitiveDownOnlyAggressive, BGPsecTransitiveTimid, 
    #            BGPsecTransitiveDownOnlyTimid, BGPsecTransitiveDownOnlyNoHashTimid]

    def __init__(*args, **kwargs):
        """Set behavior based on internal counter."""
        super(Aggregator, self).__init__(*args, **kwargs)
