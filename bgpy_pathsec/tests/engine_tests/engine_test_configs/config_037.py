from bgpy import EngineTestConfig, ASNs
from bgpy_pathsec.attacks.pathsec_scenario_config import PathsecScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_009
from ....attacks import Eavesdropper
from ....policies import BGPsecTransitiveDownOnlyAS, TransitiveDroppingNoAdoptCustomersAlwaysAS
from ....announcements import PathManipulationAnn
# from ....subgraphs import OverheadBPOAllSubgraph

config_p_037 = EngineTestConfig(
    name="P037",
    desc=(
        "GlobalEavesdropper attack with Transitive Dropping ASes with no "
        "adopting customers. Adopting customers are converted to "
        "TransitiveDroppingNeverAS nodes, except for the origin."
    ),
    scenario_config=PathsecScenarioConfig(
        ScenarioCls=Eavesdropper,
        BaseASCls=TransitiveDroppingNoAdoptCustomersAlwaysAS,
        AdoptASCls=BGPsecTransitiveDownOnlyAS,
        AnnCls=PathManipulationAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({
            1: BGPsecTransitiveDownOnlyAS,
            3: BGPsecTransitiveDownOnlyAS,
            5: BGPsecTransitiveDownOnlyAS,
            7: BGPsecTransitiveDownOnlyAS,
            777: BGPsecTransitiveDownOnlyAS,
        }),
        communities_up=False,
    ),
    graph=p_graph_009,
    propagation_rounds=3,
    # SubgraphCls=OverheadBPOAllSubgraph,
)
