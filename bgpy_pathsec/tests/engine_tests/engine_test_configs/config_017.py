from bgpy import EngineTestConfig, BGPAS, ASNs
from bgpy_pathsec.attacks.pathsec_scenario_config import PathsecScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_008
from ....attacks import IntentionalLeak
from ....policies import BGPsecTransitiveAS
from ....announcements import PathManipulationAnn


class BGPsecTransitiveWithPathShorteningDefenseAS(BGPsecTransitiveAS):
    """For use with IntentionalLeak"""
    name = "BGP-Isec with Path Shortening Defense"


config_p_017 = EngineTestConfig(
    name="P017",
    desc=(
        "Path Shortening Defense test. The attack announcement should "
        "have an AS path length of 4 (including the attacker ASN)"
    ),
    scenario_config=PathsecScenarioConfig(
        ScenarioCls=IntentionalLeak,
        AnnCls=PathManipulationAnn,
        BaseASCls=BGPAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({
            4: BGPsecTransitiveWithPathShorteningDefenseAS,
            5: BGPsecTransitiveWithPathShorteningDefenseAS,
            6: BGPsecTransitiveWithPathShorteningDefenseAS,
            7: BGPsecTransitiveWithPathShorteningDefenseAS,
            8: BGPsecTransitiveWithPathShorteningDefenseAS,
            9: BGPsecTransitiveWithPathShorteningDefenseAS,
            10: BGPsecTransitiveWithPathShorteningDefenseAS,
            11: BGPsecTransitiveWithPathShorteningDefenseAS,
            12: BGPsecTransitiveWithPathShorteningDefenseAS,
            14: BGPsecTransitiveWithPathShorteningDefenseAS,
            777: BGPsecTransitiveWithPathShorteningDefenseAS,
        }),
        no_hash=False,
        communities_up=False,
    ),
    graph=p_graph_008,
    propagation_rounds=2,
)
