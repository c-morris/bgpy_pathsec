from .intentional_leak_no_hash import IntentionalLeakNoHash

class IntentionalLeakNoHashUp(IntentionalLeakNoHash):
    """Same as IntentionalLeakNoHash, but with UP attributes.

    Now paths can be truncated to the first non-adopting ASN, but the UP
    attributes limit the effectiveness of route leaks.
    """

    def _trim_do_communities(self, ann):
        """With UP attributes, this becomes a no-op.

        The reasoning for this is as follows:
          Since the origin is always adopting, there is always at least one UP
          attribute on the announcement. If any down-only communities are also
          present, it means the UP preimage was also removed, and any leaks
          will be detected. Therefore, if any down-only communities are
          present, they should not be removed.
        """
        pass
