from ..graphs import PGraph005
from ....attacks import IntentionalLeak
from ....policies import BGPsecTransitiveAS
from ....announcements import PathManipulationAnn
from lib_bgp_simulator import EngineTestConfig, BGPAS, ASNs


class Config008(EngineTestConfig):
    """Contains config options to run a test"""

    name = "P008"
    desc = "Small Graph test"
    scenario = IntentionalLeak(attacker_asns={ASNs.ATTACKER.value},
                               victim_asns={ASNs.VICTIM.value},
                               BaseASCls=BGPAS,
                               AnnCls=PathManipulationAnn)
    graph = PGraph005()
    non_default_as_cls_dict = {1: BGPsecTransitiveAS,
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
                               777: BGPsecTransitiveAS}
    propagation_rounds = 1
