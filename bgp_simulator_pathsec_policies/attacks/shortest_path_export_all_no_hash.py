from .shortest_path_export_all import ShortestPathExportAll
from .mixins import _truncate_ann_no_hash


class ShortestPathExportAllNoHash(ShortestPathExportAll):
    """Shortest path Export all strategy, from other works.
    Only leaks a single path (the shortest one) to providers.
    Assumes no hash chain to prevent path shortening.
    """
    _truncate_ann = _truncate_ann_no_hash
