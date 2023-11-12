from dataclasses import replace

from .shortest_path_export_all import ShortestPathExportAll


class TwoHopAttack(ShortestPathExportAll):
    """Same as ShortestPathExportAllNoHash, but always do a two hop attack."""

    def _truncate_ann(self, ann):
        """Truncate to the first two ASNs."""

        new_kwargs = dict()

        new_as_path = ann.as_path

        if len(ann.as_path) > 1:
            new_as_path = ann.as_path[-2:]  # only save last two ASNs
        # check if there were signatures invalidated
        # if there were two or more signatures, at least one is now invalid
        if len(ann.bgpsec_path) > 1:
            new_kwargs["removed_signatures"] = (ann.bgpsec_path[-1],)
            # ann = replace(ann, removed_signatures=(ann.bgpsec_path[-1],))
        # update BGPsec path to match new AS path
        # ann = replace(
        #     ann,
        #     bgpsec_path=tuple([x for x in ann.bgpsec_path if x in ann.as_path]),
        # )

        new_kwargs["bgpsec_path"] = (
            tuple([x for x in ann.bgpsec_path if x in new_as_path]),
        )

        # Set the path_end attribute. This will rarely be set.
        if len(ann.as_path) < 2:
            new_kwargs["path_end_valid"] = False
            # ann = replace(ann, path_end_valid=False)
        new_kwargs["as_path"] = new_as_path
        return replace(ann, **new_kwargs)
