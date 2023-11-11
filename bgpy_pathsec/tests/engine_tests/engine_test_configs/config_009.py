from bgpy import EngineTestConfig, BGPAS, ASNs
from bgpy.simulation_framework import ScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_005
from ....attacks import IntentionalLeak
from ....policies import BGPsecTransitiveDownOnlyAS
from ....announcements import PathManipulationAnn

config_p_009 = EngineTestConfig(
    name="P009",
    desc="Graph 5 test, BGPsec Transitive Down Only",
    scenario_config=ScenarioConfig(
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
    graph=p_graph_005,
    propagation_rounds=1,
)
