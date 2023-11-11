from ..graphs import PGraph010
from ....attacks import Eavesdropper
from ....policies import BGPsecTransitiveDownOnlyEncrUpAS
from ....announcements import PathManipulationAnn
from bgpy import EngineTestConfig, BGPAS, ASNs


class Config038(EngineTestConfig):
    """Contains config options to run a test"""

    name = "P038"
    desc = "Fig 6 test, eavesdropper on otherwise unseen announcement"
    scenario = Eavesdropper(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        BaseASCls=BGPAS,
        AnnCls=PathManipulationAnn,
    )
    graph = PGraph010()
    non_default_as_cls_dict = {
        1: BGPsecTransitiveDownOnlyEncrUpAS,
        3: BGPsecTransitiveDownOnlyEncrUpAS,
        5: BGPsecTransitiveDownOnlyEncrUpAS,
        6: BGPsecTransitiveDownOnlyEncrUpAS,
        777: BGPsecTransitiveDownOnlyEncrUpAS,
    }
    propagation_rounds = 2
