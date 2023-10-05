from ..graphs import PGraph009
from ....attacks import OriginHijack
from ....policies import PathEndAS
from ....announcements import PathManipulationAnn
from ....subgraphs import OverheadBPOAllSubgraph
from bgpy import EngineTestConfig, BGPAS, ASNs


class Config029(EngineTestConfig):
    """Contains config options to run a test"""

    name = "P029"
    desc = "Fig 6 test, 1-hop attack against Path End"
    scenario = OriginHijack(attacker_asns={ASNs.ATTACKER.value},
                            victim_asns={ASNs.VICTIM.value},
                            BaseASCls=BGPAS,
                            AnnCls=PathManipulationAnn)
    graph = PGraph009()
    non_default_as_cls_dict = {1: PathEndAS,
                               2: PathEndAS,
                               3: PathEndAS,
                               4: PathEndAS,
                               5: PathEndAS,
                               7: PathEndAS,
                               777: PathEndAS}
    propagation_rounds = 1
    SubgraphCls = OverheadBPOAllSubgraph
