from lib_bgp_simulator import Prefixes, Timestamps, Relationships

from .mh_path_manipulation import MHPathManipulation


class MHLeak(MHPathManipulation):
    def _get_announcements(self, **extra_ann_kwargs):
        return [self.AnnCls(prefix=Prefixes.PREFIX.value,
                            timestamp=Timestamps.VICTIM.value,
                            as_path=(self.victim_asn,),
                            bgpsec_path=(self.victim_asn,),
                            removed_signatures=tuple(),
                            next_as=self.victim_asn,
                            do_communities=tuple(),
                            roa_valid_length=None,
                            roa_origin=None,
                            withdraw=False,
                            traceback_end=True,
                            seed_asn=self.victim_asn,
                            communities=tuple(),
                            recv_relationship=Relationships.ORIGIN)]
