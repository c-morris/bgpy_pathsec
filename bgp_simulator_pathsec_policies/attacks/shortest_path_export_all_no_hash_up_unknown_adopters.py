from .shortest_path_export_all_no_hash_up import ShortestPathExportAllNoHashUp
from .global_eavesdropper import GlobalEavesdropperUp
from .mixins import UnknownAdoptersMixin


class ShortestPathExportAllNoHashUpUnknownAdopters(UnknownAdoptersMixin, ShortestPathExportAllNoHashUp):
    """Shortest path Export all strategy, from other works.
    Only leaks a single path (the shortest one) to providers.
    This version accounts for UP attributes.
    """


class GlobalEavesdropperUpUnknownAdopters(UnknownAdoptersMixin, GlobalEavesdropperUp):
    """GlobalEavesdropper wiht Unknown Adopters.
    This version accounts for UP attributes.
    """

