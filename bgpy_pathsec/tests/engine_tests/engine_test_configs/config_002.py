from bgpy import EngineTestConfig, BGPAS, ASNs
from bgpy_pathsec.attacks.pathsec_scenario_config import PathsecScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_001
from ....attacks import IntentionalLeak
from ....policies import BGPsecTransitiveAS
from ....announcements import PathManipulationAnn

config_p_002 = EngineTestConfig(
    name="P002",
    desc=(
        "BGPsec Transitive security third preference test. "
        "AS 1 should prefer the path via AS 3."
    ),
    scenario_config=PathsecScenarioConfig(
        ScenarioCls=IntentionalLeak,
        AnnCls=PathManipulationAnn,
        BaseASCls=BGPAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({
            1: BGPsecTransitiveAS,
            3: BGPsecTransitiveAS,
            4: BGPsecTransitiveAS,
            777: BGPsecTransitiveAS,
        }),
    ),
    graph=p_graph_001,
    propagation_rounds=1,
)
