from .eavesdropper import Eavesdropper


class EavesdropperUp(Eavesdropper):
    """Attacker has visibility into other AS RIBs.
       This version assumes UP attributes.
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
