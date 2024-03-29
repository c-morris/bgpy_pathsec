from bgpy import EngineTestConfig, BGPAS, ASNs
from bgpy_pathsec.attacks.pathsec_scenario_config import PathsecScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_002
from ....attacks import IntentionalLeak
from ....policies import BGPsecTransitiveDownOnlyAS
from ....announcements import PathManipulationAnn

config_p_004 = EngineTestConfig(
    name="P004",
    desc=(
        "BGPsec Transitive Down Only contiguous adopting preference test, "
        "AS 1 should prefer the path via AS 3."
    ),
    scenario_config=PathsecScenarioConfig(
        ScenarioCls=IntentionalLeak,
        AnnCls=PathManipulationAnn,
        BaseASCls=BGPAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                1: BGPsecTransitiveDownOnlyAS,
                2: BGPsecTransitiveDownOnlyAS,
                3: BGPsecTransitiveDownOnlyAS,
                4: BGPsecTransitiveDownOnlyAS,
                7: BGPsecTransitiveDownOnlyAS,
                8: BGPsecTransitiveDownOnlyAS,
                9: BGPsecTransitiveDownOnlyAS,
                777: BGPsecTransitiveDownOnlyAS,
            }
        ),
    ),
    graph=p_graph_002,
    propagation_rounds=1,
)
