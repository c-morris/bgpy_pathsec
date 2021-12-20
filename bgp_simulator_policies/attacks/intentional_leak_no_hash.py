from .intentional_leak import IntentionalLeak

class IntentionalLeakNoHash(IntentionalLeak):
    """Same as IntentionalLeak, but without the path shortening defense.

    Now paths can be truncated to the first non-adopting ASN, yielding shorter
    paths.  
    """

    def _truncate_ann(self, ann):
        """Truncate to the first non-adopting ASN."""
        ann.as_path = ann.as_path[1:] # remove attacker ASN
        partial = ann.bgpsec_path
        full = ann.as_path
        i = len(partial) - 1
        j = len(full) - 1
        while partial[i] == full[j] and i >= 0 and j > 0:
            i -= 1
            j -= 1
        ann.as_path = ann.as_path[j:]
        # update BGPsec path to match new AS path
        ann.bgpsec_path = tuple(x for x in ann.bgpsec_path if x in ann.as_path)

