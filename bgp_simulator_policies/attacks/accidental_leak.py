from lib_bgp_simulator import BGPAS, Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario, Graph, SimulatorEngine, DataPoint, ROAValidity

from .mh_leak import MHLeak

from .. import PAnn

class AccidentalLeak(MHLeak):

    def post_propagation_hook(self, engine: SimulatorEngine, prev_data_point: DataPoint, *args, **kwargs):
        # Add the route leak from the attacker
        attacker_ann = None
        attacker_ann = engine.as_dict[self.attacker_asn]._local_rib.get_ann(Prefixes.PREFIX.value)
        if prev_data_point.propagation_round == 0:
            # If the attacker never received, the announcement, this attack is impossible, return
            if attacker_ann is None: 
                print("Attacker did not receive announcement from victim, cannot attack")
                print("Attacker RIB WAS", engine.as_dict[self.attacker_asn]._local_rib)
                return
            print("Altering the recv_relationship to customer for:", attacker_ann)
            engine.as_dict[self.attacker_asn]._local_rib.get_ann(Prefixes.PREFIX.value).recv_relationship = Relationships.CUSTOMERS
