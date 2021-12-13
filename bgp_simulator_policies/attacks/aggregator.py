from lib_bgp_simulator import Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario, Graph, SimulatorEngine, DataPoint, ROAValidity, BGPAS

from .mh_path_manipulation import MHPathManipulation
from . import OriginHijack, IntentionalLeak, IntentionalLeakNoHash
from ..policies import BGPsecAS, DownOnlyAS, BGPsecTransitiveAS, BGPsecTransitiveDownOnlyAS, BGPsecAggressiveAS, BGPsecTransitiveAggressiveAS, BGPsecTransitiveDownOnlyAggressiveAS, BGPsecTransitiveTimidAS, BGPsecTransitiveDownOnlyTimidAS, BGPsecTransitiveDownOnlyNoHashTimidAS 

# This is an aggregation of attacks and policies
# this *only* works with a specific set of policies!
# any deviation may produce unexpected results

class Aggregator(MHPathManipulation):
    pol_atk_map = { 
            BGPAS: OriginHijack,
            BGPsecAggressiveAS: OriginHijack,
            BGPsecTransitiveAggressiveAS: OriginHijack,
            BGPsecTransitiveDownOnlyAggressiveAS: OriginHijack,
            BGPsecTransitiveTimidAS: IntentionalLeak,
            BGPsecTransitiveDownOnlyTimidAS: IntentionalLeak,
            BGPsecTransitiveDownOnlyNoHashTimidAS: IntentionalLeakNoHash,
        }
    def __init__(self, *args, **kwargs):
        """Set behavior based on internal counter."""
        
        Aggregator._get_announcements = OriginHijack._get_announcements
        Aggregator._truncate_ann = self.nullfunc
        Aggregator._trim_do_communities = self.nullfunc
        super(Aggregator, self).__init__(*args, **kwargs)
    
    @staticmethod 
    def nullfunc(*args, **kwargs):
        pass

    def seed(self, engine):
        """Seeds announcement at the proper AS"""
        print('self as classes', self.adopting_as_class)
        Atk_cls = self.pol_atk_map[self.adopting_as_class]
        print('atk_cls', Atk_cls)
        # set attributes
        Aggregator._get_announcements = Atk_cls._get_announcements
        Aggregator.post_propagation_hook = Atk_cls.post_propagation_hook
        Aggregator._truncate_ann = getattr(Atk_cls, "_truncate_ann", self.nullfunc)
        Aggregator._trim_do_communities = getattr(Atk_cls, "_trim_do_communities", self.nullfunc)
        # reset anns
        self.announcements = self._get_announcements()
        return super(Aggregator, self).seed(engine)
