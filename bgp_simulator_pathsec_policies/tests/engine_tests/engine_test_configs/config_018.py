from ..graphs import PGraph008
from ....attacks import IntentionalLeak
from ....announcements import PathManipulationAnn
from bgp_simulator_pkg import EngineTestConfig, BGPAS, ASNs

from .config_017 import BGPsecTransitiveWithPathShorteningDefenseAS


class Config018(EngineTestConfig):
    """Contains config options to run a test"""

    name = "P018"
    desc = ("Path Shortening Defense test with fewer adopting ASes. "
            "The attack announcement should have an AS path length of "
            "4 (including the attacker ASN)")
    scenario = IntentionalLeak(attacker_asns={ASNs.ATTACKER.value},
                               victim_asns={ASNs.VICTIM.value},
                               BaseASCls=BGPAS,
                               AnnCls=PathManipulationAnn)
    graph = PGraph008()
    non_default_as_cls_dict = {5: BGPsecTransitiveWithPathShorteningDefenseAS,
                               6: BGPsecTransitiveWithPathShorteningDefenseAS,
                               7: BGPsecTransitiveWithPathShorteningDefenseAS,
                               8: BGPsecTransitiveWithPathShorteningDefenseAS,
                               9: BGPsecTransitiveWithPathShorteningDefenseAS,
                               10: BGPsecTransitiveWithPathShorteningDefenseAS,
                               11: BGPsecTransitiveWithPathShorteningDefenseAS,
                               12: BGPsecTransitiveWithPathShorteningDefenseAS,
                               14: BGPsecTransitiveWithPathShorteningDefenseAS,
                               777: BGPsecTransitiveWithPathShorteningDefenseAS
                               }
    propagation_rounds = 2
