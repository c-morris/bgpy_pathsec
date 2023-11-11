from ..graphs import PGraph009
from ....attacks import OriginHijack
from ....policies import BGPsecTransitiveAS
from ....announcements import PathManipulationAnn
from ....subgraphs import OverheadBPOAllSubgraph
from bgpy import EngineTestConfig, BGPAS, ASNs


class Config025(EngineTestConfig):
    """Contains config options to run a test"""

    name = "P025"
    desc = (
        "Fig 6 test, 1-hop attack to test BGPsec Transitive overhead "
        "metrics. Check shared_data YAML to confirm correctness."
    )
    scenario = OriginHijack(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        BaseASCls=BGPAS,
        AnnCls=PathManipulationAnn,
    )
    graph = PGraph009()
    non_default_as_cls_dict = {
        1: BGPsecTransitiveAS,
        2: BGPsecTransitiveAS,
        3: BGPsecTransitiveAS,
        4: BGPsecTransitiveAS,
        5: BGPsecTransitiveAS,
        6: BGPsecTransitiveAS,
        7: BGPsecTransitiveAS,
        777: BGPsecTransitiveAS,
    }
    propagation_rounds = 1
    SubgraphCls = OverheadBPOAllSubgraph
