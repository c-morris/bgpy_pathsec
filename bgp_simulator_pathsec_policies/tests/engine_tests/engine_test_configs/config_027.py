from ..graphs import PGraph009
from ....policies import BGPsecAS
from ....announcements import PathManipulationAnn
from ....subgraphs import OverheadBPOAllSubgraph
from bgpy import EngineTestConfig, BGPAS, ASNs
from bgpy import ValidPrefix


class Config027(EngineTestConfig):
    """Contains config options to run a test"""

    name = "P027"
    desc = ("Fig 6 test, 1-hop attack to test BGPsec overhead metrics with no "
            "attack. Check shared_data YAML to confirm correctness.")
    scenario = ValidPrefix(attacker_asns={ASNs.ATTACKER.value},
                           victim_asns={ASNs.VICTIM.value},
                           BaseASCls=BGPAS,
                           AnnCls=PathManipulationAnn)
    graph = PGraph009()
    non_default_as_cls_dict = {1: BGPsecAS,
                               2: BGPsecAS,
                               3: BGPsecAS,
                               4: BGPsecAS,
                               5: BGPsecAS,
                               6: BGPsecAS,
                               7: BGPsecAS,
                               777: BGPsecAS}
    propagation_rounds = 1
    SubgraphCls = OverheadBPOAllSubgraph
