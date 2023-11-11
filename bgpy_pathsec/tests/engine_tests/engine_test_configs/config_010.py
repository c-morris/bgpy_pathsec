from bgpy import EngineTestConfig, BGPAS, ASNs
from bgpy.simulation_framework import ScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_006
from ....attacks import IntentionalLeak
from ....policies import BGPsecAS
from ....announcements import PathManipulationAnn

config_p_010 = EngineTestConfig(
    name="P010",
    desc="Graph 6 test, BGPsec",
    scenario_config=ScenarioConfig(
        ScenarioCls=IntentionalLeak,
        AnnCls=PathManipulationAnn,
        BaseASCls=BGPAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({
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
        }),
    ),
    graph=p_graph_006,
    propagation_rounds=1,
)
