from bgpy import EngineTestConfig, BGPAS, ASNs
from bgpy_pathsec.attacks.pathsec_scenario_config import PathsecScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_009
from ....attacks import IntentionalLeak
from ....policies import BGPsecTransitiveDownOnlyAS
from ....announcements import PathManipulationAnn

config_p_020 = EngineTestConfig(
    name="P020",
    desc="Fig 6 test. Intentional Leak attack with no UP attributes.",
    scenario_config=PathsecScenarioConfig(
        ScenarioCls=IntentionalLeak,
        AnnCls=PathManipulationAnn,
        BaseASCls=BGPAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({
            1: BGPsecTransitiveDownOnlyAS,
            3: BGPsecTransitiveDownOnlyAS,
            5: BGPsecTransitiveDownOnlyAS,
            6: BGPsecTransitiveDownOnlyAS,
            777: BGPsecTransitiveDownOnlyAS,
        }),
        no_hash=False,
        communities_up=False,
    ),
    graph=p_graph_009,
    propagation_rounds=2,
)
