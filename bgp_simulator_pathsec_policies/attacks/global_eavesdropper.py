from bgp_simulator_pkg import Prefixes, Relationships

from .eavesdropper import Eavesdropper
from .mixins import _trim_do_communities_up


class GlobalEavesdropper(Eavesdropper):
    """Attacker has visibility into all other AS RIBs.
    """

    global_eavesdropper = True


class GlobalEavesdropperUp(GlobalEavesdropper):
    """Attacker has visibility into all other AS RIBs.
    """

    _trim_do_communities = _trim_do_communities_up
