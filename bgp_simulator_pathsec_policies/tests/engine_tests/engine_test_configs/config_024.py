from .config_022 import EavesdropperUpTest22
from ..graphs import PGraph010
from ....policies import BGPsecTransitiveDownOnlyAS
from ....announcements import PathManipulationAnn
from bgp_simulator_pkg import EngineTestConfig, BGPAS, ASNs


class Config024(EngineTestConfig):
    """Contains config options to run a test"""

    name = "P024"
    desc = "Fig 6 test, eavesdropper on otherwise unseen announcement"
    scenario = EavesdropperUpTest22(attacker_asns={ASNs.ATTACKER.value},
                                    victim_asns={ASNs.VICTIM.value},
                                    BaseASCls=BGPAS,
                                    AnnCls=PathManipulationAnn)
    graph = PGraph010()
    non_default_as_cls_dict = {1: BGPsecTransitiveDownOnlyAS,
                               3: BGPsecTransitiveDownOnlyAS,
                               5: BGPsecTransitiveDownOnlyAS,
                               6: BGPsecTransitiveDownOnlyAS,
                               777: BGPsecTransitiveDownOnlyAS}
    propagation_rounds = 2
