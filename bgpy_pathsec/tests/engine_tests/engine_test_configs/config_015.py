from bgpy import EngineTestConfig, BGPAS, ASNs
from bgpy_pathsec.attacks.pathsec_scenario_config import PathsecScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_007
from ....attacks import IntentionalLeak
from ....policies import BGPsecTransitiveDownOnlyAS
from ....announcements import PathManipulationAnn

config_p_015 = EngineTestConfig(
    name="P015",
    desc=(
        "Intentional Leak Timid-All attack, "
        "BGPsec Transitive Down Only Graph 7 test"
    ),
    scenario_config=PathsecScenarioConfig(
        ScenarioCls=IntentionalLeak,
        AnnCls=PathManipulationAnn,
        BaseASCls=BGPAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({
            1: BGPsecTransitiveDownOnlyAS,
            2: BGPsecTransitiveDownOnlyAS,
            3: BGPsecTransitiveDownOnlyAS,
            4: BGPsecTransitiveDownOnlyAS,
            5: BGPsecTransitiveDownOnlyAS,
            6: BGPsecTransitiveDownOnlyAS,
            7: BGPsecTransitiveDownOnlyAS,
            8: BGPsecTransitiveDownOnlyAS,
            9: BGPsecTransitiveDownOnlyAS,
            10: BGPsecTransitiveDownOnlyAS,
            11: BGPsecTransitiveDownOnlyAS,
            12: BGPsecTransitiveDownOnlyAS,
            14: BGPsecTransitiveDownOnlyAS,
            777: BGPsecTransitiveDownOnlyAS,
        }),
    ),
    graph=p_graph_007,
    propagation_rounds=2,
)
