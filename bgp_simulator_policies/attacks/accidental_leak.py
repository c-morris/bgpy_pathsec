from bgp_simulator_pkg import Prefixes, Relationships

from .mh_leak import MHLeak


class AccidentalLeak(MHLeak):
    """An "accidental" route leak.

    This attack is meant to approximate an accidental leak in that the attacker
    does not remove any down-only communities and does not alter the AS path.
    The unmodified announcement is simply forwarded to all of its providers.
    """

    def post_propagation_hook(self, engine,
                              propagation_round, *args, **kwargs):
        # Add the route leak from the attacker
        attacker_ann = None
        attacker_ann = engine.as_dict[list(self.attacker_asns)[0]]._local_rib.get_ann(Prefixes.PREFIX.value) # noqa E501
        if propagation_round == 1:
            # If attacker never received announcement, attack is impossible
            if attacker_ann is None:
                print("Attacker did not receive announcement from victim, cannot attack") # noqa E501
                return
            print("Altering the recv_relationship to customer for:", attacker_ann) # noqa E501
            engine.as_dict[list(self.attacker_asns)[0]]._local_rib.get_ann(Prefixes.PREFIX.value).recv_relationship = Relationships.CUSTOMERS # noqa E501
