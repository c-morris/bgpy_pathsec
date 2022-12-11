from .two_hop_attack import TwoHopAttack
from .intentional_leak_no_hash_up import IntentionalLeakNoHashUp

class TwoHopAttackUp(TwoHopAttack):
    """Same as TwoHop, but with UP attributes.
    """
TwoHopAttackUp._trim_do_communities = \
    IntentionalLeakNoHashUp._trim_do_communities
