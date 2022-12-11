from .intentional_leak_timid import IntentionalLeakTimid
from .shortest_path_export_all import ShortestPathExportAll


class ShortestPathExportAllTimid(IntentionalLeakTimid):
    """Shortest path Export all strategy, from other works.
    Only leaks a single path (the shortest one) to providers.
    Will only attack if it can leak an announcement with no DO communities.
    """

    ShortestPathExportAllTimid.leak_announcements_to_providers = \
        ShortestPathExportAll.leak_announcements_to_providers
