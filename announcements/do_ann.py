from lib_bgp_simulator import Announcement

class DOAnn(Announcement):
    """
    Down-Only Community Announcement
    https://datatracker.ietf.org/doc/html/draft-ietf-grow-route-leak-detection-mitigation-05
    """

    __slots__ = ["do_communities",]

    def __init__(self, *args, **kwargs):
        super(DOAnn, self).__init__(*args, **kwargs)
        # do_communities is a tuple of ASNs which are added to the announcement with the down-only community
        self.do_communities = tuple()


