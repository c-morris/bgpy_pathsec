from bgpy import EngineTestConfig, ASNs, BGPAS
from bgpy_pathsec.attacks.pathsec_scenario_config import PathsecScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_009
from ....attacks import Eavesdropper
from ....policies import BGPsecTransitiveDownOnlyAS
from ....announcements import PathManipulationAnn
# from ....subgraphs import OverheadBPOAllSubgraph

config_p_034 = EngineTestConfig(
    name="P034",
    desc="Global Eavesdropper test",
    scenario_config=PathsecScenarioConfig(
        ScenarioCls=Eavesdropper,
        BaseASCls=BGPAS,
        AdoptASCls=BGPsecTransitiveDownOnlyAS,
        AnnCls=PathManipulationAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({
            1: BGPsecTransitiveDownOnlyAS,
            3: BGPsecTransitiveDownOnlyAS,
            4: BGPsecTransitiveDownOnlyAS,
            5: BGPsecTransitiveDownOnlyAS,
            7: BGPsecTransitiveDownOnlyAS,
            777: BGPsecTransitiveDownOnlyAS,
        }),
        communities_up=False,
    ),
    graph=p_graph_009,
    propagation_rounds=2,
    # SubgraphCls=OverheadBPOAllSubgraph,
)
