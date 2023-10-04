from .shortest_path_export_all_no_hash_up import ShortestPathExportAllNoHashUp



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
