from .shortest_path_export_all_timid import ShortestPathExportAllTimid
from .mixins import _truncate_ann_no_hash


class ShortestPathExportAllNoHashTimid(ShortestPathExportAllTimid):
    """Shortest path Export all strategy, from other works.
    Only leaks a single path (the shortest one) to providers.
    Will only attack if it can leak an announcement with no DO communities.
    """
    _truncate_ann = _truncate_ann_no_hash
