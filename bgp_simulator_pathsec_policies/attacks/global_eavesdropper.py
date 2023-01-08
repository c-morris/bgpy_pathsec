from bgp_simulator_pkg import Prefixes, Relationships

from .eavesdropper import Eavesdropper


class GlobalEavesdropper(Eavesdropper):
    """Attacker has visibility into all other AS RIBs.
    """

    global_eavesdropper = True
