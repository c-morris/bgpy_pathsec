from ..graphs import PGraph007
from ....attacks import IntentionalLeak
from ....policies import BGPsecTransitiveAS
from ....announcements import PathManipulationAnn
from bgpy import EngineTestConfig, BGPAS, ASNs


class Config013(EngineTestConfig):
    """Contains config options to run a test"""

    name = "P013"
    desc = "Intentional Leak Timid-Path attack, BGPsec Transitive Graph 7 test"
    scenario = IntentionalLeak(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        BaseASCls=BGPAS,
        AnnCls=PathManipulationAnn,
        no_hash=False,
        communities_up=False,
    )
    graph = PGraph007()
    non_default_as_cls_dict = {
        1: BGPsecTransitiveAS,
        2: BGPsecTransitiveAS,
        3: BGPsecTransitiveAS,
        4: BGPsecTransitiveAS,
        5: BGPsecTransitiveAS,
        6: BGPsecTransitiveAS,
        7: BGPsecTransitiveAS,
        8: BGPsecTransitiveAS,
        9: BGPsecTransitiveAS,
        10: BGPsecTransitiveAS,
        11: BGPsecTransitiveAS,
        12: BGPsecTransitiveAS,
        14: BGPsecTransitiveAS,
        777: BGPsecTransitiveAS,
    }
    propagation_rounds = 2
