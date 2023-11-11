from ..graphs import PGraph009
from ....attacks import Eavesdropper
from ....policies import BGPsecTransitiveDownOnlyAS
from ....announcements import PathManipulationAnn
from bgp_simulator_pkg import EngineTestConfig, BGPAS, ASNs


class EavesdropperUpTest22(Eavesdropper):

    vantage_points = [7]


class Config022(EngineTestConfig):
    """Contains config options to run a test"""

    name = "P022"
    desc = ("Fig 6 test, eavesdropper attacker with 7 as vantage point. "
            "UP attributes do not stop the attack.")
    scenario = EavesdropperUpTest22(attacker_asns={ASNs.ATTACKER.value},
                                    victim_asns={ASNs.VICTIM.value},
                                    BaseASCls=BGPAS,
                                    AnnCls=PathManipulationAnn,
                                    no_hash=False)
    graph = PGraph009()
    non_default_as_cls_dict = {1: BGPsecTransitiveDownOnlyAS,
                               3: BGPsecTransitiveDownOnlyAS,
                               5: BGPsecTransitiveDownOnlyAS,
                               6: BGPsecTransitiveDownOnlyAS,
                               777: BGPsecTransitiveDownOnlyAS}
    propagation_rounds = 2
