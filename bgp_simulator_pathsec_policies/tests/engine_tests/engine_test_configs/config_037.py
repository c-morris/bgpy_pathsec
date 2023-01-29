from ..graphs import PGraph009
from ....attacks import GlobalEavesdropper
from ....policies import BGPsecTransitiveDownOnlyAS
from ....announcements import PathManipulationAnn
from ....subgraphs import OverheadBPOAllSubgraph
from ....policies import TransitiveDroppingNoAdoptCustomersAlwaysAS
from bgp_simulator_pkg import EngineTestConfig, ASNs, BGPAS


class Config037(EngineTestConfig):
    """Contains config options to run a test"""

    name = "P037"
    desc = "GlobalEavesdropper test"
    scenario = GlobalEavesdropper(attacker_asns={ASNs.ATTACKER.value},
                                     victim_asns={ASNs.VICTIM.value},
                                     BaseASCls=TransitiveDroppingNoAdoptCustomersAlwaysAS,
                                     AdoptASCls=BGPsecTransitiveDownOnlyAS,
                                     AnnCls=PathManipulationAnn)


    graph = PGraph009()
    non_default_as_cls_dict = {1: BGPsecTransitiveDownOnlyAS,
                               3: BGPsecTransitiveDownOnlyAS,
                               5: BGPsecTransitiveDownOnlyAS,
                               7: BGPsecTransitiveDownOnlyAS,
                               777: BGPsecTransitiveDownOnlyAS}
    propagation_rounds = 3
    SubgraphCls = OverheadBPOAllSubgraph
