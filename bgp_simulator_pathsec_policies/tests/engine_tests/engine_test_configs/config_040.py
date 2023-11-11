from ..graphs import PGraph009
from ....attacks import ShortestPathExportAll
from ....policies import KAPKFalseAlwaysAS, BGPsecTransitiveAS
from ....announcements import PathManipulationAnn
from ....subgraphs import OverheadBPOAllSubgraph
from bgp_simulator_pkg import EngineTestConfig, ASNs, BGPAS


class Config040(EngineTestConfig):
    """Contains config options to run a test"""

    name = "P040"
    desc = ("KAPK False AS test, with the origin having unknown adoption "
            "status.")
    scenario = ShortestPathExportAll(attacker_asns={ASNs.ATTACKER.value},
                                     victim_asns={ASNs.VICTIM.value},
                                     BaseASCls=BGPAS,
                                     AnnCls=PathManipulationAnn,
                                     unknown_adopter=True)
    graph = PGraph009()
    non_default_as_cls_dict = {1: BGPsecTransitiveAS,
                               2: BGPsecTransitiveAS,
                               3: BGPsecTransitiveAS,
                               4: BGPsecTransitiveAS,
                               5: BGPsecTransitiveAS,
                               6: BGPsecTransitiveAS,
                               7: KAPKFalseAlwaysAS,
                               777: BGPsecTransitiveAS}

    propagation_rounds = 1
    SubgraphCls = OverheadBPOAllSubgraph
