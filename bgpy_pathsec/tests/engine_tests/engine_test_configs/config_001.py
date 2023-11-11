from bgpy import EngineTestConfig, BGPAS, ASNs
from bgpy.simulation_framework import ScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_001
from ....attacks import IntentionalLeak
from ....policies import BGPsecAS
from ....announcements import PathManipulationAnn

config_p_001 = EngineTestConfig(
    name="P001",
    desc=(
        "BGPsec security third preference test, "
        "AS 1 should prefer the path via AS 3"
    ),
    scenario_config=ScenarioConfig(
        ScenarioCls=IntentionalLeak,
        AnnCls=PathManipulationAnn,
        BaseASCls=BGPAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({
            1: BGPsecAS,
            3: BGPsecAS,
            4: BGPsecAS,
            777: BGPsecAS,
        }),
    ),
    graph=p_graph_001,
    propagation_rounds=1,
)
