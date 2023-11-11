from bgpy import EngineTestConfig, BGPAS, ASNs
from bgpy_pathsec.attacks.pathsec_scenario_config import PathsecScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_003
from ....attacks import IntentionalLeak
from ....policies import DownOnlyAS
from ....announcements import PathManipulationAnn

config_p_005 = EngineTestConfig(
    name="P005",
    desc=(
        "Down Only attribute test. AS 1 should add a DO community "
        "when sending to AS 2 (verify in YAML)"
    ),
    scenario_config=PathsecScenarioConfig(
        ScenarioCls=IntentionalLeak,
        AnnCls=PathManipulationAnn,
        BaseASCls=BGPAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                1: DownOnlyAS,
                2: DownOnlyAS,
                3: DownOnlyAS,
                4: DownOnlyAS,
                777: DownOnlyAS,
            }
        ),
    ),
    graph=p_graph_003,
    propagation_rounds=1,
)
