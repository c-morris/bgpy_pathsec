from .shortest_path_export_all_no_hash_up import ShortestPathExportAllNoHashUp
from .global_eavesdropper import GlobalEavesdropperUp



class ShortestPathExportAllNoHashUpUnknownAdopters(ShortestPathExportAllNoHashUp):
    """Shortest path Export all strategy, from other works.
    Only leaks a single path (the shortest one) to providers.
    This version accounts for UP attributes.
    """

    def _truncate_ann(self, ann):
        """
        
        """

        old_bgpsec_path = ann.bgpsec_path
        ann.bgpsec_path = tuple()

        for _asn in old_bgpsec_path:
            if _asn not in ann.unknown_adopters:
                ann.bgpsec_path += (_asn,)

        super(ShortestPathExportAllNoHashUp, self)._truncate_ann(ann)


class GlobalEavesdropperUpUnknownAdopters(GlobalEavesdropperUp):
    """GlobalEavesdropper wiht Unknown Adopters.
    This version accounts for UP attributes.
    """

    # TODO need to find a way to do this without duplicating code
    # (cannot use a mixin function because of super)
    def _truncate_ann(self, ann):
        """
        
        """

        old_bgpsec_path = ann.bgpsec_path
        ann.bgpsec_path = tuple()

        for _asn in old_bgpsec_path:
            if _asn not in ann.unknown_adopters:
                ann.bgpsec_path += (_asn,)

        super(GlobalEavesdropperUp, self)._truncate_ann(ann)
