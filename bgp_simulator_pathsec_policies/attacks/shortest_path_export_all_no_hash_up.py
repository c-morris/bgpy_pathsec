from .shortest_path_export_all_no_hash import ShortestPathExportAllNoHash
from .mixins import _trim_do_communities_up


class ShortestPathExportAllNoHashUp(ShortestPathExportAllNoHash):
    """Shortest path Export all strategy, from other works.
    Only leaks a single path (the shortest one) to providers.
    This version of the attack accounts for UP attributes.
    """

    _trim_do_communities = _trim_do_communities_up

