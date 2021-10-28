from lib_bgp_simulator import BGPAS, Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario, Graph, SimulatorEngine, DataPoint, ROAValidity

from .mh_path_manipulation import MHPathManipulation
from .. import PAnn

class MHLeak(MHPathManipulation):
    def _get_announcements(self, **extra_ann_kwargs):
        return [self.AnnCls(prefix=Prefixes.PREFIX.value,
                            timestamp=Timestamps.VICTIM.value,
                            as_path=(self.victim_asn,),
                            bgpsec_path=(self.victim_asn,),
                            removed_signatures = tuple(),
                            next_as=self.victim_asn,
                            do_communities = tuple(),
                            roa_validity = ROAValidity.UNKNOWN,
                            withdraw = False,
                            traceback_end = True,
                            seed_asn=self.victim_asn,
                            recv_relationship=Relationships.ORIGIN)]