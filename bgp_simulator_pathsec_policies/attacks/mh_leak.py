from bgpy.bgpy import Prefixes, Timestamps, Relationships

from .mh_path_manipulation import MHPathManipulation


class MHLeak(MHPathManipulation):
    def _get_announcements(self, *args, **kwargs):
        """Returns the two announcements seeded for this engine input

        This engine input is for a prefix hijack,
        consisting of a valid prefix and invalid prefix

        for subclasses of this EngineInput, you can set AnnCls equal to
        something other than Announcement
        """

        anns = list()
        for victim_asn in self.victim_asns:
            # TODO: Determine what has replaced AnnCls
            anns.append(self.AnnCls(prefix=Prefixes.PREFIX.value,
                                    as_path=(victim_asn,),
                                    timestamp=Timestamps.VICTIM.value,
                                    seed_asn=victim_asn,
                                    roa_valid_length=True,
                                    roa_origin=victim_asn,
                                    recv_relationship=Relationships.ORIGIN,
                                    next_as=victim_asn,
                                    do_communities=tuple(),
                                    bgpsec_path=(victim_asn,),
                                    removed_signatures=tuple(),
                                    withdraw=False,
                                    traceback_end=True,
                                    communities=()
                                    ))

        err = "Fix the roa_origins of the announcements for multiple victims"
        assert len(self.victim_asns) == 1, err

        return tuple(anns)
