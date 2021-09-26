from lib_bgp_simulator import Announcement

class DOAnn(Announcement):
    """
    Down-Only Community Announcement
    https://datatracker.ietf.org/doc/html/draft-ietf-grow-route-leak-detection-mitigation-05
    """

    __slots__ = ["do_communities",]

    def __init__(self, *args, **kwargs):

        # do_communities is a tuple of ASNs which are added to the announcement with the down-only community
        self.do_communities = kwargs.pop("do_communities", tuple())
        super(DOAnn, self).__init__(*args, **kwargs)

    @property
    def default_copy_kwargs(self):
        """Returns default copy attributes"""

        kwargs = super(DOAnn, self).default_copy_kwargs
        kwargs.update({"do_communities": self.do_communities})
        return kwargs
