from ..graphs import PGraph009
from ....attacks import Eavesdropper
from ....policies import BGPsecTransitiveDownOnlyAS
from ....announcements import PathManipulationAnn
from ....subgraphs import OverheadBPOAllSubgraph
from ....policies import TransitiveDroppingNoAdoptCustomersAlwaysAS
from bgpy import EngineTestConfig, ASNs


class Config037(EngineTestConfig):
    """Contains config options to run a test"""

    name = "P037"
    desc = (
        "GlobalEavesdropper attack with Transitive Dropping ASes with no "
        "adopting customers. Adopting customers are converted to "
        "TransitiveDroppingNeverAS nodes, except for the origin."
    )
    scenario = Eavesdropper(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        BaseASCls=TransitiveDroppingNoAdoptCustomersAlwaysAS,  # noqa E501
        AdoptASCls=BGPsecTransitiveDownOnlyAS,
        AnnCls=PathManipulationAnn,
        communities_up=False,
    )
    graph = PGraph009()
    non_default_as_cls_dict = {
        1: BGPsecTransitiveDownOnlyAS,
        3: BGPsecTransitiveDownOnlyAS,
        5: BGPsecTransitiveDownOnlyAS,
        7: BGPsecTransitiveDownOnlyAS,
        777: BGPsecTransitiveDownOnlyAS,
    }
    propagation_rounds = 3
    SubgraphCls = OverheadBPOAllSubgraph
