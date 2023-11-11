from bgpy import EngineTestConfig, ASNs, BGPAS
from bgpy_pathsec.attacks.pathsec_scenario_config import PathsecScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_009
from ....attacks import Eavesdropper
from ....policies import BGPsecTransitiveDownOnlyEncrUpAS
from ....announcements import PathManipulationAnn
# from ....subgraphs import OverheadBPOAllSubgraph

config_p_035 = EngineTestConfig(
    name="P035",
    desc="GlobalEavesdropper with Encrypted UP attributes test",
    scenario_config=PathsecScenarioConfig(
        ScenarioCls=Eavesdropper,
        BaseASCls=BGPAS,
        AdoptASCls=BGPsecTransitiveDownOnlyEncrUpAS,
        AnnCls=PathManipulationAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({
            1: BGPsecTransitiveDownOnlyEncrUpAS,
            3: BGPsecTransitiveDownOnlyEncrUpAS,
            4: BGPsecTransitiveDownOnlyEncrUpAS,
            5: BGPsecTransitiveDownOnlyEncrUpAS,
            7: BGPsecTransitiveDownOnlyEncrUpAS,
            777: BGPsecTransitiveDownOnlyEncrUpAS,
        }),
        no_hash=False,
    ),
    graph=p_graph_009,
    propagation_rounds=2,
    # SubgraphCls=OverheadBPOAllSubgraph,
)
