from bgpy import Scenario, Prefixes, Relationships, Timestamps

from ..policies import BGPsecAS, BGPsecTransitiveAS
from ..policies import TransitiveDroppingNoAdoptCustomersAS


class MHPathManipulation(Scenario):

    def _get_announcements(self, *args, **kwargs):
        """Returns the two announcements seeded for this engine input

        This engine input is for a prefix hijack,
        consisting of a valid prefix and invalid prefix

        for subclasses of this EngineInput, you can set AnnCls equal to
        something other than Announcement
        """

        anns = list()
        for victim_asn in self.victim_asns:
            anns.append(
                self.scenario_config.AnnCls(
                    prefix=Prefixes.PREFIX.value,
                    as_path=(victim_asn,),
                    timestamp=Timestamps.VICTIM.value,
                    seed_asn=victim_asn,
                    roa_valid_length=True,
                    roa_origin=victim_asn,
                    recv_relationship=Relationships.ORIGIN,
                )
            )

        err = "Fix the roa_origins of the announcements for multiple victims"
        assert len(self.victim_asns) == 1, err

        return tuple(anns)

    def setup_engine(self, *args, **kwargs):
        """Setup engine. Also clear BGPsec Performance Metric Counters."""

        BGPsecAS.count = 0
        BGPsecAS.bpo_count = 0
        BGPsecTransitiveAS.count = 0
        BGPsecTransitiveAS.bpo_count = 0
        TransitiveDroppingNoAdoptCustomersAS.convert_count = 0
        super().setup_engine(*args, **kwargs)
