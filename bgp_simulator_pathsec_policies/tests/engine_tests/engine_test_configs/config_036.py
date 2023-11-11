from ..graphs import PGraph012
from ....attacks import Eavesdropper
from ....policies import BGPsecTransitiveDownOnlyAS
from ....announcements import PathManipulationAnn
from ....subgraphs import OverheadBPOAllSubgraph
from bgp_simulator_pkg import EngineTestConfig, ASNs, BGPAS


class Config036(EngineTestConfig):
    """Contains config options to run a test"""

    name = "P036"
    desc = ("GlobalEavesdropper with otherwise unseen announcement test. "
            "The attack announcement should be from AS 8.")
    scenario = Eavesdropper(attacker_asns={ASNs.ATTACKER.value},
                            victim_asns={ASNs.VICTIM.value},
                            BaseASCls=BGPAS,
                            AdoptASCls=BGPsecTransitiveDownOnlyAS,
                            AnnCls=PathManipulationAnn,
                            no_hash=False,
                            communities_up=False)
    graph = PGraph012()
    non_default_as_cls_dict = {1: BGPsecTransitiveDownOnlyAS,
                               2: BGPsecTransitiveDownOnlyAS,
                               3: BGPsecTransitiveDownOnlyAS,
                               4: BGPsecTransitiveDownOnlyAS,
                               5: BGPsecTransitiveDownOnlyAS,
                               7: BGPsecTransitiveDownOnlyAS,
                               777: BGPsecTransitiveDownOnlyAS}
    propagation_rounds = 2
    SubgraphCls = OverheadBPOAllSubgraph
