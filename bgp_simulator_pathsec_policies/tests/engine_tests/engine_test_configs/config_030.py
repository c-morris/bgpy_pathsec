from ..graphs import PGraph009
from ....attacks import OriginHijack
from ....policies import BGPsecTransitiveAS
from ....announcements import PathManipulationAnn
from ....subgraphs import OverheadBPOAllSubgraph
from bgp_simulator_pkg import EngineTestConfig, BGPAS, ASNs


class Config030(EngineTestConfig):
    """Contains config options to run a test"""

    name = "P030"
    desc = "Fig 6 test, BGPsecTransitiveAS, Overhead subgraph"
    scenario = OriginHijack(attacker_asns={ASNs.ATTACKER.value},
                            victim_asns={ASNs.VICTIM.value},
                            BaseASCls=BGPAS,
                            AnnCls=PathManipulationAnn)
    graph = PGraph009()
    non_default_as_cls_dict = {1: BGPsecTransitiveAS,
                               2: BGPsecTransitiveAS,
                               3: BGPsecTransitiveAS,
                               4: BGPsecTransitiveAS,
                               5: BGPsecTransitiveAS,
                               7: BGPsecTransitiveAS,
                               777: BGPsecTransitiveAS}
    propagation_rounds = 1
    SubgraphCls = OverheadBPOAllSubgraph
