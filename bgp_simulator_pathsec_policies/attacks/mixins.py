# Mix-In methods for including in attack classes

def _trim_do_communities_up(self, ann):
    """With UP attributes, this becomes a no-op.

    The reasoning for this is as follows:
      Since the origin is always adopting, there is always at least one UP
      attribute on the announcement. If any down-only communities are also
      present, it means the UP preimage was also removed, and any leaks
      will be detected. Therefore, if any down-only communities are
      present, they should not be removed.
    """
    pass


def _truncate_ann_no_hash(self, ann):
    """Truncate to the first non-adopting ASN."""
    ann.as_path = ann.as_path[1:]  # remove attacker ASN
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
