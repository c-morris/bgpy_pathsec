from ..graphs import PGraph011
from ....attacks import ShortestPathExportAll
from ....policies import TransitiveDroppingAlwaysAS, BGPsecTransitiveAS
from ....announcements import PathManipulationAnn
from ....subgraphs import OverheadBPOAllSubgraph
from bgpy import EngineTestConfig, ASNs, BGPAS


class Config032(EngineTestConfig):
    """Contains config options to run a test"""

    name = "P032"
    desc = "Transitive Dropping AS test, with fewer adopting ASes"
    scenario = ShortestPathExportAll(attacker_asns={ASNs.ATTACKER.value},
                                     victim_asns={ASNs.VICTIM.value},
                                     BaseASCls=TransitiveDroppingAlwaysAS,
                                     AdoptASCls=BGPsecTransitiveAS,
                                     AnnCls=PathManipulationAnn)
    graph = PGraph011()
    non_default_as_cls_dict = {2: BGPAS,
                               3: BGPsecTransitiveAS,
                               5: BGPAS,
                               6: BGPAS,
                               7: BGPsecTransitiveAS,
                               9: BGPsecTransitiveAS,
                               777: BGPsecTransitiveAS}
    propagation_rounds = 1
    SubgraphCls = OverheadBPOAllSubgraph
