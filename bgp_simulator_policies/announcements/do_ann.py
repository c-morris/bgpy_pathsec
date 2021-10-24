from dataclasses import dataclass

from lib_bgp_simulator import Announcement

@dataclass(eq=False)
class DOAnn(Announcement):
    """
    Down-Only Community Announcement
    https://datatracker.ietf.org/doc/html/draft-ietf-grow-route-leak-detection-mitigation-05
    """

    __slots__ = ("do_communities",)

    # do_communities is a tuple of ASNs which are added to the announcement with the down-only community
    do_communities: tuple
