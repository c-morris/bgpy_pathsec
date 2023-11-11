from bgpy import EngineTestConfig, BGPAS, ASNs
from bgpy.simulation_framework import ScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_010
from .config_022 import EavesdropperUpTest22
from ....policies import BGPsecTransitiveDownOnlyAS
from ....announcements import PathManipulationAnn

config_p_024 = EngineTestConfig(
    name="P024",
    desc="Fig 6 test, eavesdropper on otherwise unseen announcement",
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
    ),
    graph=p_graph_010,
    propagation_rounds=2,
)
