from lib_bgp_simulator import BGPAS, Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario, Graph, SimulatorEngine, DataPoint, ROAValidity

from .mh_path_manipulation import MHPathManipulation
from .. import PAnn

class ErrTest(MHPathManipulation):
    def _get_announcements(self, **extra_ann_kwargs):
        return [self.AnnCls(prefix=Prefixes.PREFIX.value,
                            timestamp=Timestamps.VICTIM.value,
                            as_path=(12808,),
                            bgpsec_path=(12808,),
                            removed_signatures = tuple(),
                            next_as=12808,
                            do_communities = tuple(),
                            roa_validity = ROAValidity.UNKNOWN,
                            withdraw = False,
                            traceback_end = True,
                            seed_asn=12808,
                            communities = tuple(),
                            recv_relationship=Relationships.ORIGIN)]
