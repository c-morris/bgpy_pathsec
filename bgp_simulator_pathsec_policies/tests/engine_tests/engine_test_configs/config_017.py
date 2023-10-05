from ..graphs import PGraph008
from ....attacks import IntentionalLeak
from ....policies import BGPsecTransitiveAS
from ....announcements import PathManipulationAnn
from bgpy import EngineTestConfig, BGPAS, ASNs


class BGPsecTransitiveWithPathShorteningDefenseAS(BGPsecTransitiveAS):
    """For use with IntentionalLeak"""
    name = "BGP-Isec with Path Shortening Defense"


class Config017(EngineTestConfig):
    """Contains config options to run a test"""

    name = "P017"
    desc = ("Path Shortening Defense test. The attack announcement should "
            "have an AS path length of 4 (including the attacker ASN)")
    scenario = IntentionalLeak(attacker_asns={ASNs.ATTACKER.value},
                               victim_asns={ASNs.VICTIM.value},
                               BaseASCls=BGPAS,
                               AnnCls=PathManipulationAnn)
    graph = PGraph008()
    non_default_as_cls_dict = {4: BGPsecTransitiveWithPathShorteningDefenseAS,
                               5: BGPsecTransitiveWithPathShorteningDefenseAS,
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
