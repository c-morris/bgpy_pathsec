from bgpy import EngineTestConfig, BGPAS, ASNs, ValidPrefix
from bgpy.simulation_framework import ScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_009
from ....policies import BGPsecAS
from ....announcements import PathManipulationAnn
# from ....subgraphs import OverheadBPOAllSubgraph

config_p_027 = EngineTestConfig(
    name="P027",
    desc=(
        "Fig 6 test, 1-hop attack to test BGPsec overhead metrics with no "
        "attack. Check shared_data YAML to confirm correctness."
    ),
    scenario_config=ScenarioConfig(
        ScenarioCls=ValidPrefix,
        AnnCls=PathManipulationAnn,
        BaseASCls=BGPAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({
            1: BGPsecAS,
            2: BGPsecAS,
            3: BGPsecAS,
            4: BGPsecAS,
            5: BGPsecAS,
            6: BGPsecAS,
            7: BGPsecAS,
            777: BGPsecAS,
        }),
    ),
    graph=p_graph_009,
    propagation_rounds=1,
    # SubgraphCls=OverheadBPOAllSubgraph,
)
