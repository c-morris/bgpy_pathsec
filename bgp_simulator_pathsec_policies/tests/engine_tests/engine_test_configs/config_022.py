from ..graphs import PGraph009
from ....attacks import EavesdropperUp
from ....policies import BGPsecTransitiveDownOnlyAS
from ....announcements import PathManipulationAnn
from bgp_simulator_pkg import EngineTestConfig, BGPAS, ASNs


class EavesdropperUpTest22(EavesdropperUp):

    vantage_points = [7]


class Config022(EngineTestConfig):
    """Contains config options to run a test"""

    name = "P022"
    desc = "Fig 6 test, eavesdropper, 7 as vantage point"
    scenario = EavesdropperUpTest22(attacker_asns={ASNs.ATTACKER.value},
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
