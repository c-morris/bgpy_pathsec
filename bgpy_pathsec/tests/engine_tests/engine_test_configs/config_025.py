from bgpy import EngineTestConfig, BGPAS, ASNs
from bgpy.simulation_framework import ScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_009
from ....attacks import OriginHijack
from ....policies import BGPsecTransitiveAS
from ....announcements import PathManipulationAnn
from ....subgraphs import OverheadBPOAllSubgraph

config_p_025 = EngineTestConfig(
    name="P025",
    desc=(
        "Fig 6 test, 1-hop attack to test BGPsec Transitive overhead "
        "metrics. Check shared_data YAML to confirm correctness."
    ),
    scenario_config=ScenarioConfig(
        ScenarioCls=OriginHijack,
        AnnCls=PathManipulationAnn,
        BaseASCls=BGPAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({
            1: BGPsecTransitiveAS,
            2: BGPsecTransitiveAS,
            3: BGPsecTransitiveAS,
            4: BGPsecTransitiveAS,
            5: BGPsecTransitiveAS,
            6: BGPsecTransitiveAS,
            7: BGPsecTransitiveAS,
            777: BGPsecTransitiveAS,
        }),
    ),
    graph=p_graph_009,
    propagation_rounds=1,
    # SubgraphCls=OverheadBPOAllSubgraph,
)
