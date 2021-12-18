import types

from lib_bgp_simulator import Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario, Graph, SimulatorEngine, DataPoint, ROAValidity, BGPAS

from .mh_path_manipulation import MHPathManipulation
from . import OriginHijack, IntentionalLeak, IntentionalLeakNoHash
from ..policies import BGPsecAS, DownOnlyAS, BGPsecTransitiveAS, BGPsecTransitiveDownOnlyAS, BGPsecAggressiveAS, BGPsecTransitiveAggressiveAS, BGPsecTransitiveDownOnlyAggressiveAS, BGPsecTransitiveTimidAS, BGPsecTransitiveDownOnlyTimidAS, BGPsecTransitiveDownOnlyNoHashTimidAS 

# This is an aggregation of attacks and policies
# this *only* works with a specific set of policies!
# any deviation may produce unexpected results

class Aggregator(OriginHijack):
    
    def __init__(self, *args, **kwargs):
        """Set behavior based on internal counter."""
        self.pol_atk_map = { 
            BGPAS: OriginHijack,
            BGPsecAggressiveAS: OriginHijack,
            BGPsecTransitiveAggressiveAS: OriginHijack,
            BGPsecTransitiveDownOnlyAggressiveAS: OriginHijack,
            BGPsecTransitiveTimidAS: IntentionalLeak,
            BGPsecTransitiveDownOnlyTimidAS: IntentionalLeak,
            BGPsecTransitiveDownOnlyNoHashTimidAS: IntentionalLeakNoHash,
        }
        super(Aggregator, self).__init__(*args, **kwargs)
    
    def nullfunc(*args, **kwargs):
        pass
    def _truncate_ann(*args, **kwargs):
        pass
    def _trim_do_communities(*args, **kwargs):
        pass

    def seed(self, engine, AdoptingASClass=None):
        """Seeds announcement at the proper AS"""
        Atk_cls = self.pol_atk_map[AdoptingASClass]
        # set attributes
        #self._get_announcements = types.MethodType(Atk_cls._get_announcements, self)
        #self.post_propagation_hook = types.MethodType(Atk_cls.post_propagation_hook, self)
        #self._truncate_ann = types.MethodType(getattr(Atk_cls, "_truncate_ann", self.nullfunc), self)
        #self._trim_do_communities = types.MethodType(getattr(Atk_cls, "_trim_do_communities", self.nullfunc), self)
        Aggregator._get_announcements = Atk_cls._get_announcements
        Aggregator.post_propagation_hook = Atk_cls.post_propagation_hook
        Aggregator._truncate_ann = getattr(Atk_cls, "_truncate_ann", self.nullfunc)
        Aggregator._trim_do_communities = getattr(Atk_cls, "_trim_do_communities", self.nullfunc)
        # reset anns
        #print('before', self.announcements)
        self.announcements = self._get_announcements()
        #print('after', self.announcements)
        return super(Aggregator, self).seed(engine)
