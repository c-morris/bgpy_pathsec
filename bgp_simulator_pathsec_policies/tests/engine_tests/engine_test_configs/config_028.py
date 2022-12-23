from ..graphs import PGraph001
from ....attacks import ShortestPathExportAll
from ....policies import TransitiveDroppingAlwaysAS, BGPsecTransitiveAS
from ....announcements import PathManipulationAnn
from bgp_simulator_pkg import EngineTestConfig, ASNs


class Config028(EngineTestConfig):
    """Contains config options to run a test"""

    name = "P028"
    desc = "TransitiveDroppingAs test"
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

    def _get_engine(self, scenario):
        """Enforce specific transitive dropping ASes before the test runs"""
        engine = super(Config028, self)._get_engine(scenario)
        engine.as_dict[5].transitive_dropping = True
        return engine
