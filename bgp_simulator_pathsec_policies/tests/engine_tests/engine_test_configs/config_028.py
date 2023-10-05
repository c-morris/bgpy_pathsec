from ..graphs import PGraph001
from ....attacks import ShortestPathExportAll
from ....policies import TransitiveDroppingAlwaysAS, BGPsecTransitiveAS
from ....announcements import PathManipulationAnn
from ....subgraphs import OverheadBPOAllSubgraph
from bgpy import EngineTestConfig, ASNs


class Config028(EngineTestConfig):
    """Contains config options to run a test"""

    name = "P028"
    desc = ("TransitiveDroppingAS test. "
            "AS 2 should choose the longer path from its provider.")
    scenario = ShortestPathExportAll(attacker_asns={ASNs.ATTACKER.value},
                                     victim_asns={ASNs.VICTIM.value},
                                     BaseASCls=TransitiveDroppingAlwaysAS,
                                     AnnCls=PathManipulationAnn)
    graph = PGraph001()
    non_default_as_cls_dict = {1: BGPsecTransitiveAS,
                               2: BGPsecTransitiveAS,
                               3: BGPsecTransitiveAS,
                               4: BGPsecTransitiveAS,
                               777: BGPsecTransitiveAS}
    propagation_rounds = 1
    SubgraphCls = OverheadBPOAllSubgraph
