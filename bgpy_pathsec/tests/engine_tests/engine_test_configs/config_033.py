from bgpy import EngineTestConfig, ASNs, BGPAS
from bgpy.simulation_framework import ScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_011
from ....attacks import ShortestPathExportAll
from ....policies import TransitiveDroppingAlwaysAS, BGPsecTransitiveAS
from ....announcements import PathManipulationAnn
# from ....subgraphs import OverheadBPOAllSubgraph

config_p_033 = EngineTestConfig(
    name="P033",
    desc=(
        "Transitive Dropping AS test, with AS 2 dropping transitive "
        "attributes."
    ),
    scenario_config=ScenarioConfig(
        ScenarioCls=ShortestPathExportAll,
        BaseASCls=TransitiveDroppingAlwaysAS,
        AdoptASCls=BGPsecTransitiveAS,
        AnnCls=PathManipulationAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({
            3: BGPsecTransitiveAS,
            5: BGPAS,
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
