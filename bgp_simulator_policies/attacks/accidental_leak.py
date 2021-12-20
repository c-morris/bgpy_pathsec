from lib_bgp_simulator import Prefixes, Relationships, SimulatorEngine, DataPoint

from .mh_leak import MHLeak

class AccidentalLeak(MHLeak):
    """An "accidental" route leak.

    This attack is meant to approximate an accidental leak in that the attacker
    does not remove any down-only communities and does not alter the AS path.
    The unmodified announcement is simply forwarded to all of its providers. 
    """

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
