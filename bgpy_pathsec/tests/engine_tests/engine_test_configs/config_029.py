from bgpy import EngineTestConfig, BGPAS, ASNs
from bgpy_pathsec.attacks.pathsec_scenario_config import PathsecScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_009
from ....attacks import OriginHijack
from ....policies import PathEndAS
from ....announcements import PathManipulationAnn

# from ....subgraphs import OverheadBPOAllSubgraph

config_p_029 = EngineTestConfig(
    name="P029",
    desc="Fig 6 test, 1-hop attack against Path End",
    scenario_config=PathsecScenarioConfig(
        ScenarioCls=OriginHijack,
        AnnCls=PathManipulationAnn,
        BaseASCls=BGPAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                1: PathEndAS,
                2: PathEndAS,
                3: PathEndAS,
                4: PathEndAS,
                5: PathEndAS,
                7: PathEndAS,
                777: PathEndAS,
            }
        ),
    ),
    graph=p_graph_009,
    propagation_rounds=1,
    # SubgraphCls=OverheadBPOAllSubgraph,
)
