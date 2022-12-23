from .intentional_leak_no_hash import IntentionalLeakNoHash
from .mixins import _trim_do_communities_up


class IntentionalLeakNoHashUp(IntentionalLeakNoHash):
    """Same as IntentionalLeakNoHash, but with UP attributes.

    Now paths can be truncated to the first non-adopting ASN, but the UP
    attributes limit the effectiveness of route leaks.
    """

    _trim_do_communities = _trim_do_communities_up
