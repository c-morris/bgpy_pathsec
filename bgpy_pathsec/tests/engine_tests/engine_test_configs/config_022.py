from bgpy import EngineTestConfig, BGPAS, ASNs
from bgpy.simulation_framework import ScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_009
from ....policies import BGPsecTransitiveDownOnlyAS
from ....announcements import PathManipulationAnn


class EavesdropperUpTest22(Eavesdropper):
    vantage_points = [7]


config_p_022 = EngineTestConfig(
    name="P022",
    desc=(
        "Fig 6 test, eavesdropper attacker with 7 as vantage point. "
        "UP attributes do not stop the attack."
    ),
    scenario_config=ScenarioConfig(
        ScenarioCls=EavesdropperUpTest22,
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
        communities_up=False,
        no_hash=False,
    ),
    graph=p_graph_009,
    propagation_rounds=2,
)
