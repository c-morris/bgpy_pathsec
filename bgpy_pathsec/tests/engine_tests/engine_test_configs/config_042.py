from bgpy import EngineTestConfig, BGPAS, ASNs
from bgpy.simulation_framework import ScenarioConfig
from frozendict import frozendict


from ..graphs import p_graph_009
from ....attacks import ShortestPathExportAll
from ....policies import KAPKFalseAlwaysAS, BGPsecTransitiveAS
from ....announcements import PathManipulationAnn
# from ....subgraphs import OverheadBPOAllSubgraph

config_p_042 = EngineTestConfig(
    name="P042",
    desc = (
        "KAPK False AS test, with the origin having unknown adoption " "status."
    )
    scenario_config=ScenarioConfig(
        ScenarioCls=ShortestPathExportAll,
        AnnCls=PathManipulationAnn,
        BaseASCls=BGPAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({
            1: BGPsecTransitiveAS,
            2: KAPKFalseAlwaysAS,
            3: BGPsecTransitiveAS,
            4: BGPsecTransitiveAS,
            5: BGPsecTransitiveAS,
            6: BGPsecTransitiveAS,
            7: KAPKFalseAlwaysAS,
            777: BGPsecTransitiveAS,
        }),
        unknown_adopter=True
    ),
    graph=p_graph_009,
    propagation_rounds=1,
    # SubgraphCls = OverheadBPOAllSubgraph
)

