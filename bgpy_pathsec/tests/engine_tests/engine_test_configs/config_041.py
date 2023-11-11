from bgpy import EngineTestConfig, BGPAS, ASNs
from bgpy.simulation_framework import ScenarioConfig
from frozendict import frozendict


from ..graphs import p_graph_009
from ....attacks import Eavesdropper
from ....policies import KAPKFalseAlwaysAS, BGPsecTransitiveAS
from ....announcements import PathManipulationAnn
# from ....subgraphs import OverheadBPOAllSubgraph

config_p_041 = EngineTestConfig(
    name="P041",
    desc = (
        "KAPK False AS test, with the origin having unknown adoption " "status."
    )
    scenario_config=ScenarioConfig(
        ScenarioCls=Eavesdropper,
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
            7: KAPKFalseAlwaysAS,
            777: BGPsecTransitiveAS,
        }),
        unknown_adopter=True
    ),
    graph=p_graph_009,
    propagation_rounds=1,
    # SubgraphCls = OverheadBPOAllSubgraph
)
