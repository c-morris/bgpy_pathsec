from bgpy import EngineTestConfig, BGPAS, ASNs
from bgpy_pathsec.attacks.pathsec_scenario_config import PathsecScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_008
from ....attacks import IntentionalLeak
from ....policies import BGPsecTransitiveAS
from ....announcements import PathManipulationAnn

config_p_019 = EngineTestConfig(
    name="P019",
    desc=(
        "BGPsec Transitive with no Path Shortening Defense test. "
        "The attack AS path should be shortened to the first "
        "non-adopting AS, which is 1 in this scenario."
    ),
    scenario_config=PathsecScenarioConfig(
        ScenarioCls=IntentionalLeak,
        AnnCls=PathManipulationAnn,
        BaseASCls=BGPAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({
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
        communities_up=False,
    ),
    graph=p_graph_008,
    propagation_rounds=2,
)
