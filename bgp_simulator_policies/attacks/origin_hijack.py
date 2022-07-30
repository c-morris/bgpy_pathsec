from lib_bgp_simulator import Prefixes, Timestamps, Relationships

from .mh_path_manipulation import MHPathManipulation


class OriginHijack(MHPathManipulation):
    """Origin hijack with a *fake* path"""

    def _get_announcements(self):
        """Returns the two announcements seeded for this engine input

        This engine input is for a prefix hijack,
        consisting of a valid prefix and invalid prefix

        for subclasses of this EngineInput, you can set AnnCls equal to
        something other than Announcement
        """

        anns = list()
        for victim_asn in self.victim_asns:
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
                                    withdraw = False,
                                    traceback_end = True,
                                    communities = ()
                                    ))

        err = "Fix the roa_origins of the announcements for multiple victims"
        assert len(self.victim_asns) == 1, err

        roa_origin = next(iter(self.victim_asns))

        for attacker_asn in self.attacker_asns:
            anns.append(self.AnnCls(prefix=Prefixes.PREFIX.value,
                                    as_path=(attacker_asn,),
                                    timestamp=Timestamps.ATTACKER.value,
                                    seed_asn=attacker_asn,
                                    roa_valid_length=True,
                                    roa_origin=victim_asn,
                                    recv_relationship=Relationships.ORIGIN,
                                    next_as=0,
                                    do_communities=tuple(),
                                    bgpsec_path=tuple(),
                                    removed_signatures=(list(self.victim_asns)[0],),
                                    withdraw=False,
                                    traceback_end=True,
                                    communities=tuple()
                                    ))

        return tuple(anns)
    #def _get_announcements(self, **extra_ann_kwargs):
    #    return [self.AnnCls(prefix=Prefixes.PREFIX.value,
    #                        timestamp=Timestamps.VICTIM.value,
    #                        as_path=(victim_asn,),
    #                        # Legitimate announcement has valid BGPsec attrs
    #                        bgpsec_path=(self.victim_asn,),
    #                        next_as=self.victim_asn,
    #                        removed_signatures=tuple(),
    #                        do_communities=tuple(),
    #                        roa_valid_length=None,
    #                        roa_origin=None,
    #                        withdraw=False,
    #                        traceback_end=True,
    #                        seed_asn=victim_asn,
    #                        communities=tuple(),
    #                        recv_relationship=Relationships.ORIGIN),
    #            self.AnnCls(prefix=Prefixes.PREFIX.value,
    #                        timestamp=Timestamps.ATTACKER.value,
    #                        as_path=(self.attacker_asn, victim_asn),
    #                        bgpsec_path=tuple(),
    #                        next_as=0,
    #                        do_communities=tuple(),
    #                        roa_valid_length=None,
    #                        roa_origin=None,
    #                        withdraw=False,
    #                        traceback_end=True,
    #                        seed_asn=self.attacker_asn,
    #                        # Add victim to removed signatures
    #                        removed_signatures=(self.victim_asn,),
    #                        communities=tuple(),
    #                        recv_relationship=Relationships.ORIGIN)]
