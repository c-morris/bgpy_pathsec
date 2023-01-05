from ..graphs import PGraph011
from ....attacks import ShortestPathExportAll
from ....policies import TransitiveDroppingAlwaysAS, BGPsecTransitiveAS
from ....announcements import PathManipulationAnn
from ....subgraphs import OverheadBPOAllSubgraph
from bgp_simulator_pkg import EngineTestConfig, ASNs, BGPAS


class Config031(EngineTestConfig):
    """Contains config options to run a test"""

    name = "P031"
    desc = "TransitiveDroppingAs test"
    scenario = ShortestPathExportAll(attacker_asns={ASNs.ATTACKER.value},
                                     victim_asns={ASNs.VICTIM.value},
                                     BaseASCls=TransitiveDroppingAlwaysAS,
                                     AdoptASCls=BGPsecTransitiveAS,
                                     AnnCls=PathManipulationAnn)
    graph = PGraph011()
    non_default_as_cls_dict = {2: BGPsecTransitiveAS,
                               3: BGPsecTransitiveAS,
                               5: BGPsecTransitiveAS,
                               6: BGPAS,
                               7: BGPsecTransitiveAS,
                               9: BGPsecTransitiveAS,
                               777: BGPsecTransitiveAS}
    propagation_rounds = 1
    SubgraphCls = OverheadBPOAllSubgraph
