from ..graphs import PGraph009
from ....attacks import IntentionalLeak
from ....policies import BGPsecTransitiveDownOnlyAS
from ....announcements import PathManipulationAnn
from bgp_simulator_pkg import EngineTestConfig, BGPAS, ASNs


class Config020(EngineTestConfig):
    """Contains config options to run a test"""

    name = "P020"
    desc = "Fig 6 test. Intentional Leak attack with no UP attributes."
    scenario = IntentionalLeak(attacker_asns={ASNs.ATTACKER.value},
                               victim_asns={ASNs.VICTIM.value},
                               BaseASCls=BGPAS,
                               AnnCls=PathManipulationAnn,
                               no_hash=False,
                               communities_up=False)
    graph = PGraph009()
    non_default_as_cls_dict = {1: BGPsecTransitiveDownOnlyAS,
                               3: BGPsecTransitiveDownOnlyAS,
                               5: BGPsecTransitiveDownOnlyAS,
                               6: BGPsecTransitiveDownOnlyAS,
                               777: BGPsecTransitiveDownOnlyAS}
    propagation_rounds = 2
