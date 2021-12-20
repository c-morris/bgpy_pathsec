from dataclasses import dataclass

from lib_bgp_simulator import Announcement, Relationships, ROAValidity

from .do_ann import DOAnn

@dataclass(eq=False)
class PathManipulationAnn(DOAnn):
    """
    Generic path manipulation announcement.
    """

    __slots__ = ("bgpsec_path", "next_as", "removed_signatures")



    # The BGPsec path is like the BGPsec_PATH attribute with some
    # modifications. First, unlike in real BGPsec, it can coexist with the
    # AS_PATH. This simplifies the interaction between BGPsec and legacy
    # ASes because the BGPsec ASes do not need to check their neighbor's
    # capabilities before sending an announcement. If the BGPsec and AS
    # paths are ever out of sync, that indicates it has passed through a
    # legacy AS and the BGPsec path should be ignored (except for
    # transitive BGPsec). 
    #self.bgpsec_path = kwargs.pop("bgpsec_path", tuple())
    bgpsec_path: tuple

    # The next_as indicates the AS this announcement is being sent to. It
    # must match for the announcement to be accepted. 
    #self.next_as = kwargs.pop("next_as", 0)
    next_as: int

    # The removed_signatures attribute is for tracking removed bgpsec
    # transitive signatures. Normally, a BGPsec Transitive AS would be
    # aware of all other adopting nodes and it could check for missing
    # signatures that way. For convenience, since this is a simulation,
    # attackers will update this attribute when they remove signatures. 
    #self.removed_signatures =  kwargs.pop("removed_signatures", tuple())
    removed_signatures: tuple

# We set equal to false here so that it can inherit __eq__ from parent
@dataclass(eq=False)
class PTestAnn(PathManipulationAnn):
    prefix: str = None
    as_path: tuple = None
    timestamp: int = 0
    seed_asn: int = None
    roa_validity: ROAValidity = ROAValidity.UNKNOWN
    recv_relationship: Relationships = Relationships.CUSTOMERS
    withdraw: bool = False
    traceback_end: bool = False
    do_communities: tuple = tuple()
    communities: tuple = tuple()
    bgpsec_path: tuple = tuple()
    removed_signatures: tuple = tuple()
    next_as: int = 0
