from bgpy import EngineTestConfig, ASNs, BGPAS
from bgpy_pathsec.attacks.pathsec_scenario_config import PathsecScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_011
from ....attacks import ShortestPathExportAll
from ....policies import TransitiveDroppingAlwaysAS, BGPsecTransitiveAS
from ....announcements import PathManipulationAnn
# from ....subgraphs import OverheadBPOAllSubgraph

config_p_031 = EngineTestConfig(
    name="P031",
    desc="Transitive Dropping AS test",
    scenario_config=PathsecScenarioConfig(
        ScenarioCls=ShortestPathExportAll,
        BaseASCls=TransitiveDroppingAlwaysAS,
        AdoptASCls=BGPsecTransitiveAS,
        AnnCls=PathManipulationAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({
            2: BGPsecTransitiveAS,
            3: BGPsecTransitiveAS,
            5: BGPsecTransitiveAS,
            6: BGPAS,
            7: BGPsecTransitiveAS,
            9: BGPsecTransitiveAS,
            777: BGPsecTransitiveAS,
        }),
    ),
    graph=p_graph_011,
    propagation_rounds=1,
    # SubgraphCls=OverheadBPOAllSubgraph,
)
