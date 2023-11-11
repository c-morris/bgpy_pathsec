from ..graphs import PGraph003
from ....attacks import IntentionalLeak
from ....policies import DownOnlyAS
from ....announcements import PathManipulationAnn
from bgpy import EngineTestConfig, BGPAS, ASNs


class Config005(EngineTestConfig):
    """Contains config options to run a test"""

    name = "P005"
    desc = (
        "Down Only attribute test. AS 1 should add a DO community "
        "when sending to AS 2 (verify in YAML)"
    )
    scenario = IntentionalLeak(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        BaseASCls=BGPAS,
        AnnCls=PathManipulationAnn,
    )
    graph = PGraph003()
    non_default_as_cls_dict = {
        1: DownOnlyAS,
        2: DownOnlyAS,
        3: DownOnlyAS,
        4: DownOnlyAS,
        777: DownOnlyAS,
    }
    propagation_rounds = 1
