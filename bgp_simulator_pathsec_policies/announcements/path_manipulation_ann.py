from yamlable import yaml_info
from typing import Optional, Tuple

from bgp_simulator_pkg import Relationships
from bgp_simulator_pkg import Announcement


@yaml_info(yaml_tag="PathManipulationAnn")
class PathManipulationAnn(Announcement):
    """
    Generic path manipulation announcement.
    """

    __slots__ = ("do_communities",
                 "up_pre",
                 "bgpsec_path",
                 "next_as",
                 "removed_signatures",
                 "path_end_valid")

    def __init__(self,
                 *,
                 prefix: str,
                 as_path: Tuple[int, ...],
                 timestamp: int,
                 seed_asn: int,
                 roa_valid_length: Optional[bool],
                 roa_origin: Optional[int],
                 recv_relationship: Relationships,
                 next_as: int = 0,
                 withdraw: bool = False,
                 traceback_end: bool = False,
                 communities: Tuple[str, ...] = (),
                 do_communities: Tuple[int, ...] = (),
                 up_pre: bool = True,
                 bgpsec_path: Tuple[int, ...] = (),
                 removed_signatures: Tuple[int, ...] = (),
                 path_end_valid: bool = True):
        self.prefix: str = prefix
        self.as_path: Tuple[int, ...] = as_path
        self.timestamp: int = timestamp
        self.seed_asn: int = seed_asn
        self.roa_valid_length: Optional[bool] = roa_valid_length
        self.roa_origin: Optional[int] = roa_origin
        self.recv_relationship: Relationships = recv_relationship
        self.withdraw: bool = withdraw
        self.traceback_end: bool = traceback_end
        self.communities: Tuple[str, ...] = communities
        self.do_communities: Tuple[int, ...] = do_communities
        self.up_pre: bool = up_pre
        self.bgpsec_path: Tuple[int, ...] = bgpsec_path
        self.next_as: int = next_as
        self.removed_signatures: Tuple[int, ...] = removed_signatures
        self.path_end_valid: bool = path_end_valid

    # The BGPsec path is like the BGPsec_PATH attribute with some
    # modifications. First, unlike in real BGPsec, it can coexist with the
    # AS_PATH. This simplifies the interaction between BGPsec and legacy
    # ASes because the BGPsec ASes do not need to check their neighbor's
    # capabilities before sending an announcement. If the BGPsec and AS
    # paths are ever out of sync, that indicates it has passed through a
    # legacy AS and the BGPsec path should be ignored (except for
    # transitive BGPsec).

    # The next_as indicates the AS this announcement is being sent to. It
    # must match for the announcement to be accepted.

    # The removed_signatures attribute is for tracking removed bgpsec
    # transitive signatures. Normally, a BGPsec Transitive AS would be
    # aware of all other adopting nodes and it could check for missing
    # signatures that way. For convenience, since this is a simulation,
    # attackers will update this attribute when they remove signatures.

    # The path_end_valid attribute indicates whether the first two ASes (the
    # origin and the AS immediately following it) on the path are valid
    # according to the path_end record in the RPKI for this prefix/origin pair.
    # Note, the attacker must update this attribute if modifying the
    # announcement in a way that would make an announcement invalid by path
    # end. See https://dl.acm.org/doi/pdf/10.1145/2934872.2934883 for details
    # of the path end mechanism.

    # The do_communities and up_pre attributes are for route leak prevention.
