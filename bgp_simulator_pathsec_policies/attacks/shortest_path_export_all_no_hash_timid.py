from .intentional_leak_no_hash import IntentionalLeakNoHash
from .shortest_path_export_all_timid import ShortestPathExportAllTimid


class ShortestPathExportAllNoHashTimid(ShortestPathExportAllTimid):
    """Shortest path Export all strategy, from other works.
    Only leaks a single path (the shortest one) to providers.
    Will only attack if it can leak an announcement with no DO communities.
    """
ShortestPathExportAllNoHashTimid._truncate_ann = \
    IntentionalLeakNoHash._truncate_ann
