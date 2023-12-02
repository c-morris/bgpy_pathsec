from bgpy import EngineTestConfig, BGPAS, ASNs
from bgpy_pathsec.attacks.pathsec_scenario_config import PathsecScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_005
from ....attacks import IntentionalLeak
from ....policies import BGPsecAS
from ....announcements import PathManipulationAnn

config_p_007 = EngineTestConfig(
    name="P007",
    desc="Small Graph test, BGPsec",
    scenario_config=PathsecScenarioConfig(
        ScenarioCls=IntentionalLeak,
        AnnCls=PathManipulationAnn,
        BaseASCls=BGPAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                1: BGPsecAS,
                2: BGPsecAS,
                3: BGPsecAS,
                4: BGPsecAS,
                5: BGPsecAS,
                6: BGPsecAS,
                7: BGPsecAS,
                8: BGPsecAS,
                9: BGPsecAS,
                10: BGPsecAS,
                11: BGPsecAS,
                12: BGPsecAS,
                14: BGPsecAS,
                777: BGPsecAS,
            }
        ),
    ),
    graph=p_graph_005,
    propagation_rounds=1,
)
