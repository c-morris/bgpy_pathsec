from .intentional_leak import IntentionalLeak
from .mixins import leak_announcements_to_providers_spea


class ShortestPathExportAll(IntentionalLeak):
    """Shortest path Export all strategy, from other works.
    Only leaks a single path (the shortest one) to providers.
    """

    leak_announcements_to_providers = leak_announcements_to_providers_spea
