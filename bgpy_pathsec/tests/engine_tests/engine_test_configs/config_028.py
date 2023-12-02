from bgpy import EngineTestConfig, ASNs
from bgpy_pathsec.attacks.pathsec_scenario_config import PathsecScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_001
from ....attacks import ShortestPathExportAll
from ....policies import TransitiveDroppingAlwaysAS, BGPsecTransitiveAS
from ....announcements import PathManipulationAnn

# from ....subgraphs import OverheadBPOAllSubgraph

config_p_028 = EngineTestConfig(
    name="P028",
    desc=(
        "TransitiveDroppingAS test. "
        "AS 2 should choose the longer path from its provider."
    ),
    scenario_config=PathsecScenarioConfig(
        ScenarioCls=ShortestPathExportAll,
        BaseASCls=TransitiveDroppingAlwaysAS,
        AnnCls=PathManipulationAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                1: BGPsecTransitiveAS,
                2: BGPsecTransitiveAS,
                3: BGPsecTransitiveAS,
                4: BGPsecTransitiveAS,
                777: BGPsecTransitiveAS,
            }
        ),
    ),
    graph=p_graph_001,
    propagation_rounds=1,
    # SubgraphCls=OverheadBPOAllSubgraph,
)
