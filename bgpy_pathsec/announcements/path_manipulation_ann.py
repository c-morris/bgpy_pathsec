from dataclasses import dataclass
from typing import Tuple

from yamlable import yaml_info

from bgpy import Announcement


@yaml_info(yaml_tag="PathManipulationAnn")
@dataclass(frozen=True, slots=True)
class PathManipulationAnn(Announcement):
    """
    Generic path manipulation announcement.
    """

    next_as: int = 0
    do_communities: Tuple[int, ...] = ()
    up_pre: bool = True
    bgpsec_path: Tuple[int, ...] = ()
    removed_signatures: Tuple[int, ...] = ()
    path_end_valid: bool = True
    unknown_adopters: Tuple[int, ...] = ()

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
