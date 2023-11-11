from bgpy import EngineTestConfig, BGPAS, ASNs
from bgpy.simulation_framework import ScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_010
from ....attacks import Eavesdropper
from ....policies import BGPsecTransitiveDownOnlyEncrUpAS
from ....announcements import PathManipulationAnn


config_p_038 = EngineTestConfig(
    name="P038",
    desc = (
        "Fig 6 test, eavesdropper on otherwise unseen announcement"
    )
    scenario_config=ScenarioConfig(
        ScenarioCls=Eavesdropper,
        AnnCls=PathManipulationAnn,
        BaseASCls=BGPAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({
            1: BGPsecTransitiveDownOnlyEncrUpAS,
            3: BGPsecTransitiveDownOnlyEncrUpAS,
            5: BGPsecTransitiveDownOnlyEncrUpAS,
            6: BGPsecTransitiveDownOnlyEncrUpAS,
            777: BGPsecTransitiveDownOnlyEncrUpAS,
        }),
    ),
    graph=graph_010,
    propagation_rounds=2,
)
