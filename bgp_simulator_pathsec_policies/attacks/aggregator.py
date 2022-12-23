from bgp_simulator_pkg import BGPAS

from . import OriginHijack, IntentionalLeak, IntentionalLeakNoHash
from . import IntentionalLeakTimid
from ..policies import BGPsecAS, DownOnlyAS, BGPsecTransitiveAS # noqa F401
from ..policies import BGPsecTransitiveDownOnlyAS, BGPsecAggressiveAS # noqa F401
from ..policies import BGPsecTimidAS
from ..policies import BGPsecTransitiveAggressiveAS
from ..policies import BGPsecTransitiveDownOnlyAggressiveAS
from ..policies import BGPsecTransitiveTimidAS
from ..policies import BGPsecTransitiveDownOnlyTimidAS
from ..policies import BGPsecTransitiveDownOnlyNoHashTimidAS
from ..policies import BGPsecTransitiveDownOnlyTimidLeakAS
from ..policies import BGPsecTransitiveDownOnlyNoHashAggressiveAS


class Aggregator(OriginHijack):
    """An aggregation of attacks and policies.

    This *only* works with a specific set of policies!
    any deviation may produce unexpected results.

    The idea here is to combine multiple different attacks with specific
    policies so they can all be compared on a single graph. The pol_atk_map
    determines which attack is done on each policy. Only one attack can be
    mapped to a policy, so to perform multiple attacks on a single policy,
    subclass it and change its name. This is a requirement because otherwise
    the legend entries would be identical and confusing (and there is no
    sensible automated way to combine the names).

    """

    def __init__(self, *args, **kwargs):
        """Set behavior based on internal counter."""
        self.pol_atk_map = {
            BGPAS: OriginHijack,
            BGPsecAggressiveAS: OriginHijack,
            BGPsecTimidAS: IntentionalLeak,
            BGPsecTransitiveAggressiveAS: OriginHijack,
            BGPsecTransitiveDownOnlyAggressiveAS: OriginHijack,
            BGPsecTransitiveTimidAS: IntentionalLeak,
            BGPsecTransitiveDownOnlyTimidAS: IntentionalLeak,
            BGPsecTransitiveDownOnlyNoHashTimidAS: IntentionalLeakNoHash,
            BGPsecTransitiveDownOnlyNoHashAggressiveAS: OriginHijack,
            BGPsecTransitiveDownOnlyTimidLeakAS: IntentionalLeakTimid,
        }
        super(Aggregator, self).__init__(*args, **kwargs)

    def nullfunc(*args, **kwargs):
        """Does nothing, successfully."""
        pass

    def _truncate_ann(*args, **kwargs):
        """Placeholder function. Makes this pickleable"""
        pass

    def _trim_do_communities(*args, **kwargs):
        """Placeholder function. Makes this pickleable"""
        pass

    def seed(self, engine, AdoptingASClass=None):
        """Set attack behavior and seeds announcement at the proper AS"""
        Atk_cls = self.pol_atk_map[AdoptingASClass]
        # Set attributes
        Aggregator._get_announcements = Atk_cls._get_announcements
        Aggregator.post_propagation_hook = Atk_cls.post_propagation_hook
        # These are not always defined, so they default to the null function
        Aggregator._truncate_ann = getattr(Atk_cls, "_truncate_ann", self.nullfunc) # noqa E501
        Aggregator._trim_do_communities = getattr(Atk_cls, "_trim_do_communities", self.nullfunc) # noqa E501
        # Reset anns
        self.announcements = self._get_announcements()
        return super(Aggregator, self).seed(engine)
