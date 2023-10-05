from ..graphs import PGraph009
from ....attacks import IntentionalLeakNoHashUp
from ....policies import BGPsecTransitiveDownOnlyAS
from ....announcements import PathManipulationAnn
from bgpy import EngineTestConfig, BGPAS, ASNs


class Config021(EngineTestConfig):
    """Contains config options to run a test"""

    name = "P021"
    desc = ("Fig 6 test, Intentional Leak "
            "attack with UP attributes but no path shortening defense.")
    scenario = IntentionalLeakNoHashUp(attacker_asns={ASNs.ATTACKER.value},
                                       victim_asns={ASNs.VICTIM.value},
                                       BaseASCls=BGPAS,
                                       AnnCls=PathManipulationAnn)
    graph = PGraph009()
    non_default_as_cls_dict = {1: BGPsecTransitiveDownOnlyAS,
                               3: BGPsecTransitiveDownOnlyAS,
                               5: BGPsecTransitiveDownOnlyAS,
                               6: BGPsecTransitiveDownOnlyAS,
                               777: BGPsecTransitiveDownOnlyAS}
    propagation_rounds = 2
