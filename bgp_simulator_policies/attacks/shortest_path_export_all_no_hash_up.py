from .shortest_path_export_all_no_hash import ShortestPathExportAllNoHash


class ShortestPathExportAllNoHashUp(ShortestPathExportAllNoHash):
    """Shortest path Export all strategy, from other works.
    Only leaks a single path (the shortest one) to providers.
    This version of the attack accounts for UP attributes.
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
