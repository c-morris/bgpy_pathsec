from ..graphs import PGraph008
from ....attacks import IntentionalLeak
from ....policies import BGPsecTransitiveAS
from ....announcements import PathManipulationAnn
from bgp_simulator_pkg import EngineTestConfig, BGPAS, ASNs


class Config019(EngineTestConfig):
    """Contains config options to run a test"""

    name = "P019"
    desc = ("BGPsec Transitive with no Path Shortening Defense test. "
            "The attack AS path should be shortened to the first "
            "non-adopting AS, which is 1 in this scenario.")
    scenario = IntentionalLeak(attacker_asns={ASNs.ATTACKER.value},
                               victim_asns={ASNs.VICTIM.value},
                               BaseASCls=BGPAS,
                               AnnCls=PathManipulationAnn,
                               communities_up=False)
    graph = PGraph008()
    non_default_as_cls_dict = {5: BGPsecTransitiveAS,
                               6: BGPsecTransitiveAS,
                               7: BGPsecTransitiveAS,
                               8: BGPsecTransitiveAS,
                               9: BGPsecTransitiveAS,
                               10: BGPsecTransitiveAS,
                               11: BGPsecTransitiveAS,
                               12: BGPsecTransitiveAS,
                               14: BGPsecTransitiveAS,
                               777: BGPsecTransitiveAS}
    propagation_rounds = 2
