from ..graphs import PGraph003
from ....attacks import IntentionalLeak
from ....policies import BGPsecTransitiveDownOnlyAS
from ....announcements import PathManipulationAnn
from bgpy import EngineTestConfig, BGPAS, ASNs


class Config006(EngineTestConfig):
    """Contains config options to run a test"""

    name = "P006"
    desc = ("Down Only with BGPsec Transitive Attributes test. "
            "Confirm in YAML all attributes are set correctly.")
    scenario = IntentionalLeak(attacker_asns={ASNs.ATTACKER.value},
                               victim_asns={ASNs.VICTIM.value},
                               BaseASCls=BGPAS,
                               AnnCls=PathManipulationAnn)
    graph = PGraph003()
    non_default_as_cls_dict = {1: BGPsecTransitiveDownOnlyAS,
                               2: BGPsecTransitiveDownOnlyAS,
                               3: BGPsecTransitiveDownOnlyAS,
                               4: BGPsecTransitiveDownOnlyAS,
                               777: BGPsecTransitiveDownOnlyAS}
    propagation_rounds = 1
