from bgp_simulator_pkg import Scenario, Prefixes, Relationships, Timestamps


class MHPathManipulation(Scenario):

    __slots__ = ()

    def _get_possible_attacker_asns(self,
                                    engine,
                                    percent_adoption,
                                    prev_scenario):
        """Returns possible attacker ASNs, defaulted from stubs_and_mh"""
        # Return only Multihome ASes
        return set([x.asn for x in engine if x.multihomed])

    def _get_possible_victim_asns(self,
                                  engine,
                                  percent_adoption: float,
                                  prev_scenario) -> set:
        """Returns possible victim ASNs, defaulted from stubs_and_mh"""

        return set([x.asn for x in engine if x.multihomed])

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
                                    recv_relationship=Relationships.ORIGIN))

        err = "Fix the roa_origins of the announcements for multiple victims"
        assert len(self.victim_asns) == 1, err

        return tuple(anns)
