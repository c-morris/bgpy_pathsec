from .intentional_leak import IntentionalLeak
from .mixins import _truncate_ann_no_hash


class IntentionalLeakNoHash(IntentionalLeak):
    """Same as IntentionalLeak, but without the path shortening defense.

    Now paths can be truncated to the first non-adopting ASN, yielding shorter
    paths.
    """

    _truncate_ann = _truncate_ann_no_hash
