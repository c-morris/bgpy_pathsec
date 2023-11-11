from ..graphs import PGraph009
from ....attacks import Eavesdropper
from ....policies import BGPsecTransitiveDownOnlyAS
from ....announcements import PathManipulationAnn
from ....subgraphs import OverheadBPOAllSubgraph
from bgp_simulator_pkg import EngineTestConfig, ASNs, BGPAS


class Config034(EngineTestConfig):
    """Contains config options to run a test"""

    name = "P034"
    desc = "Global Eavesdropper test"
    scenario = Eavesdropper(attacker_asns={ASNs.ATTACKER.value},
                            victim_asns={ASNs.VICTIM.value},
                            BaseASCls=BGPAS,
                            AdoptASCls=BGPsecTransitiveDownOnlyAS,
                            AnnCls=PathManipulationAnn,
                            communities_up=False)
    graph = PGraph009()
    non_default_as_cls_dict = {1: BGPsecTransitiveDownOnlyAS,
                               3: BGPsecTransitiveDownOnlyAS,
                               4: BGPsecTransitiveDownOnlyAS,
                               5: BGPsecTransitiveDownOnlyAS,
                               7: BGPsecTransitiveDownOnlyAS,
                               777: BGPsecTransitiveDownOnlyAS}
    propagation_rounds = 2
    SubgraphCls = OverheadBPOAllSubgraph
