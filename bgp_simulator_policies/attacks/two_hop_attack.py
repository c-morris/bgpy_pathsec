from .shortest_path_export_all_no_hash import ShortestPathExportAllNoHash


class TwoHopAttack(ShortestPathExportAllNoHash):
    """Same as ShortestPathExportAllNoHash, but always do a two hop attack.
    """

    def _truncate_ann(self, ann):
        """Truncate to the first two ASNs."""
        if len(ann.as_path) > 1:
            ann.as_path = ann.as_path[-2:]  # only save last two ASNs
        # update BGPsec path to match new AS path
        ann.bgpsec_path = tuple(x for x in ann.bgpsec_path if x in ann.as_path)
        # Set the path_end attribute. This will rarely be set.
        if len(ann.as_path) < 2:
            ann.path_end_valid = False
