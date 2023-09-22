from .shortest_path_export_all_up import ShortestPathExportAllUp


class ShortestPathExportAllUpUnknownAdopters(ShortestPathExportAllUp):
    """Shortest path Export all strategy, from other works.
    Only leaks a single path (the shortest one) to providers.
    This version accounts for UP attributes.
    """

    def _truncate_ann(self, ann):
        """
        
        """

        ann_to_send = ann.copy()
        ann_to_send.bgpsec_path = tuple()

        for _asn in ann.bgpsec_path:
            if _asn not in ann.unknown_adopters:
                ann_to_send.bgpsec_path += (_asn,)

        super(ShortestPathExportAllUp, self)._truncate_ann(ann_to_send)

        ann.bgpsec_path = ann_to_send.as_path