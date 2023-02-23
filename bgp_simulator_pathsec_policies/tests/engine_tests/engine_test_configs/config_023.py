from ..graphs import PGraph009
from ....attacks import IntentionalLeakNoHashUp
from ....policies import BGPsecTransitiveDownOnlyAS
from ....announcements import PathManipulationAnn
from bgp_simulator_pkg import EngineTestConfig, BGPAS, ASNs


class Config023(EngineTestConfig):
    """Contains config options to run a test"""

    name = "P023"
    desc = "Duplicate of P021, to be removed"
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
