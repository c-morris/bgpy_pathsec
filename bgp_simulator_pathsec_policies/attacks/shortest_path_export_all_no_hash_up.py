from .shortest_path_export_all_no_hash import ShortestPathExportAllNoHash
from .intentional_leak_no_hash_up import IntentionalLeakNoHashUp


class ShortestPathExportAllNoHashUp(ShortestPathExportAllNoHash):
    """Shortest path Export all strategy, from other works.
    Only leaks a single path (the shortest one) to providers.
    This version of the attack accounts for UP attributes.
    """

ShortestPathExportAllNoHashUp._trim_do_communities = \
    IntentionalLeakNoHashUp._trim_do_communities
