from bgpy import EngineTestConfig, BGPAS, ASNs
from bgpy.simulation_framework import ScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_002
from ....attacks import IntentionalLeak
from ....policies import BGPsecTransitiveAS
from ....announcements import PathManipulationAnn

config_p_003 = EngineTestConfig(
    name="P003",
    desc=(
        "BGPsec Transitive contiguous adopting preference test, "
        "AS 1 should prefer the path via AS 3."
    ),
    scenario_config=ScenarioConfig(
        ScenarioCls=IntentionalLeak,
        AnnCls=PathManipulationAnn,
        BaseASCls=BGPAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({
            1: BGPsecTransitiveAS,
            2: BGPsecTransitiveAS,
            3: BGPsecTransitiveAS,
            4: BGPsecTransitiveAS,
            7: BGPsecTransitiveAS,
            8: BGPsecTransitiveAS,
            9: BGPsecTransitiveAS,
            777: BGPsecTransitiveAS,
        }),
    ),
    graph=p_graph_002,
    propagation_rounds=1,
)
