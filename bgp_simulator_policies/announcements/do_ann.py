from dataclasses import dataclass

from lib_bgp_simulator import Announcement

@dataclass(eq=False)
class DOAnn(Announcement):
    """
    Down-Only Community Announcement
    https://datatracker.ietf.org/doc/html/draft-ietf-grow-route-leak-detection-mitigation-05
    """

    __slots__ = ["do_communities",]

    # do_communities is a tuple of ASNs which are added to the announcement with the down-only community
    #self.do_communities = kwargs.pop("do_communities", tuple())
    do_communities: tuple

    @property
    def default_copy_kwargs(self):
        """Returns default copy attributes"""

        kwargs = super(DOAnn, self).default_copy_kwargs
        kwargs.update({"do_communities": self.do_communities})
        return kwargs
