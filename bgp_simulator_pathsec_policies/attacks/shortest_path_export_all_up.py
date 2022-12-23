from .shortest_path_export_all import ShortestPathExportAll
from .mixins import _trim_do_communities_up


class ShortestPathExportAllUp(ShortestPathExportAll):
    """Shortest path Export all strategy, from other works.
    Only leaks a single path (the shortest one) to providers.
    This version accounts for UP attributes.
    """

    _trim_do_communities = _trim_do_communities_up
