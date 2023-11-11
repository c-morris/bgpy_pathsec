from bgpy import EngineTestConfig, ASNs, BGPAS
from bgpy.simulation_framework import ScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_012
from ....attacks import Eavesdropper
from ....policies import BGPsecTransitiveDownOnlyAS
from ....announcements import PathManipulationAnn
# from ....subgraphs import OverheadBPOAllSubgraph

config_p_036 = EngineTestConfig(
    name="P036",
    desc=(
        "GlobalEavesdropper with otherwise unseen announcement test. "
        "The attack announcement should be from AS 8."
    ),
    scenario_config=ScenarioConfig(
        ScenarioCls=Eavesdropper,
        BaseASCls=BGPAS,
        AdoptASCls=BGPsecTransitiveDownOnlyAS,
        AnnCls=PathManipulationAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({
            1: BGPsecTransitiveDownOnlyAS,
            2: BGPsecTransitiveDownOnlyAS,
            3: BGPsecTransitiveDownOnlyAS,
            4: BGPsecTransitiveDownOnlyAS,
            5: BGPsecTransitiveDownOnlyAS,
            7: BGPsecTransitiveDownOnlyAS,
            777: BGPsecTransitiveDownOnlyAS,
        }),
        no_hash=False,
        communities_up=False,
    ),
    graph=p_graph_012,
    propagation_rounds=2,
    # SubgraphCls=OverheadBPOAllSubgraph,
)
