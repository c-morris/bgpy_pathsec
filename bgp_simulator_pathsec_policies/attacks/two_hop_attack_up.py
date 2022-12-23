from .two_hop_attack import TwoHopAttack
from .mixins import _trim_do_communities_up


class TwoHopAttackUp(TwoHopAttack):
    """Same as TwoHop, but with UP attributes.
    """
    _trim_do_communities = _trim_do_communities_up
