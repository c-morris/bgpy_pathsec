from bgpy import EngineTestConfig, BGPAS, ASNs
from bgpy_pathsec.attacks.pathsec_scenario_config import PathsecScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_006
from ....attacks import IntentionalLeak
from ....policies import BGPsecTransitiveAS
from ....announcements import PathManipulationAnn

config_p_011 = EngineTestConfig(
    name="P011",
    desc="Graph 6 test, BGPsec Transitive",
    scenario_config=PathsecScenarioConfig(
        ScenarioCls=IntentionalLeak,
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
            7: BGPsecTransitiveAS,
            8: BGPsecTransitiveAS,
            9: BGPsecTransitiveAS,
            10: BGPsecTransitiveAS,
            11: BGPsecTransitiveAS,
            12: BGPsecTransitiveAS,
            14: BGPsecTransitiveAS,
            777: BGPsecTransitiveAS,
        }),
    ),
    graph=p_graph_006,
    propagation_rounds=1,
)
