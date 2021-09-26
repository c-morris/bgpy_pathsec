from lib_bgp_simulator import Announcement
from .do_ann import DOAnn

class PAnn(DOAnn):
    """
    Generic path manipulation announcement.
    """

    __slots__ = ["bgpsec_path", "next_as"]

    def __init__(self, *args, **kwargs):


        # The BGPsec path is like the BGPsec_PATH attribute with some
        # modifications. First, unlike in real BGPsec, it can coexist with the
        # AS_PATH. This simplifies the interaction between BGPsec and legacy
        # ASes because the BGPsec ASes do not need to check their neighbor's
        # capabilities before sending an announcement. If the BGPsec and AS
        # paths are ever out of sync, that indicates it has passed through a
        # legacy AS and the BGPsec path should be ignored (except for
        # transitive BGPsec). 
        self.bgpsec_path = kwargs.pop("bgpsec_path", tuple())

        # The next_as indicates the AS this announcement is being sent to. It
        # must match for the announcement to be accepted. 
        self.next_as = kwargs.pop("next_as", 0)

        super(PAnn, self).__init__(*args, **kwargs)
    @property
    def default_copy_kwargs(self):
        kwargs = super(PAnn, self).default_copy_kwargs
        kwargs.update({"bgpsec_path": self.bgpsec_path, "next_as": self.next_as})
        return kwargs
