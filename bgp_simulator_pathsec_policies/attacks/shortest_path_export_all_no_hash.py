from .intentional_leak_no_hash import IntentionalLeakNoHash
from .shortest_path_export_all import ShortestPathExportAll


class ShortestPathExportAllNoHash(IntentionalLeakNoHash, ShortestPathExportAll):
    """Shortest path Export all strategy, from other works.
    Only leaks a single path (the shortest one) to providers.
    Assumes no hash chain to prevent path shortening.
    """
