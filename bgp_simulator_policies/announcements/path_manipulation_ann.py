from lib_bgp_simulator import Announcement
from .do_ann import DOAnn

class PAnn(DOAnn):
    """
    Generic path manipulation announcement.
    """

    __slots__ = []

    def __init__(self, *args, **kwargs):
        super(PAnn, self).__init__(*args, **kwargs)
        # TODO: BGPsec etc stuff goes here

