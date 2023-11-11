from bgpy import EngineTestConfig, BGPAS, ASNs
from bgpy_pathsec.attacks.pathsec_scenario_config import PathsecScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_009
from ....attacks import OriginHijack
from ....policies import BGPsecAS
from ....announcements import PathManipulationAnn
# from ....subgraphs import OverheadBPOAllSubgraph

config_p_026 = EngineTestConfig(
    name="P026",
    desc=(
        "Fig 6 test, 1-hop attack to test BGPsec overhead metrics. "
        "Check shared_data YAML to confirm correctness."
    ),
    scenario_config=PathsecScenarioConfig(
        ScenarioCls=OriginHijack,
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
