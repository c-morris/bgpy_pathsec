from bgpy import EngineTestConfig, ASNs, BGPAS
from bgpy_pathsec.attacks.pathsec_scenario_config import PathsecScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_009

# from ....attacks import Eavesdropper
from ....policies import (
    BGPsecTransitiveDownOnlyAS,
    TransitiveDroppingNeverAS,
    TransitiveDroppingAlwaysAS,
)
from ....attacks import TransitiveDroppingNoAdoptCustomers
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
        ScenarioCls=TransitiveDroppingNoAdoptCustomers,
        BaseASCls=BGPAS,
        AdoptASCls=BGPsecTransitiveDownOnlyAS,
        AnnCls=PathManipulationAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                1: BGPsecTransitiveDownOnlyAS,
                2: TransitiveDroppingAlwaysAS,
                3: TransitiveDroppingNeverAS,
                4: TransitiveDroppingAlwaysAS,
                5: BGPsecTransitiveDownOnlyAS,
                7: TransitiveDroppingNeverAS,
                777: BGPsecTransitiveDownOnlyAS,
            }
        ),
        communities_up=False,
    ),
    graph=p_graph_009,
    propagation_rounds=3,
    # SubgraphCls=OverheadBPOAllSubgraph,
)
