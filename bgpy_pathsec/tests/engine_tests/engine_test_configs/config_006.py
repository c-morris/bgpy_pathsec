from bgpy import EngineTestConfig, BGPAS, ASNs
from bgpy_pathsec.attacks.pathsec_scenario_config import PathsecScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_003
from ....attacks import IntentionalLeak
from ....policies import BGPsecTransitiveDownOnlyAS
from ....announcements import PathManipulationAnn

config_p_006 = EngineTestConfig(
    name="P006",
    desc=(
        "Down Only with BGPsec Transitive Attributes test. "
        "Confirm in YAML all attributes are set correctly."
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
            777: BGPsecTransitiveDownOnlyAS,
        }),
    ),
    graph=p_graph_003,
    propagation_rounds=1,
)
