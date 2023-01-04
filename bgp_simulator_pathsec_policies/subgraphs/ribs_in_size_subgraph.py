from bgp_simulator_pkg import Subgraph
from bgp_simulator_pkg import Scenario


class RibsInSizeSubgraph(Subgraph):
    """A graph for average number of announcements in the Adj RIBs In for all
    ASes.
    """

    name: str = "ribs_in_size_all"

    def _get_subgraph_key(self,
                          scenario: Scenario,
                          *args) -> str:  # type: ignore
        """Returns the key to be used in shared_data on the subgraph"""

        return f"ribs_in_size_all" # noqa E509

    @property
    def y_axis_label(self) -> str:
        """returns y axis label"""

        return "Avg # Anns in RIBs In"


class RibsInSizeAdoptingSubgraph(RibsInSizeSubgraph):
    """A graph for average number of announcements in the Adj RIBs In for
    adopting ASes.
    """

    name: str = "ribs_in_size_adopting"

    def _get_subgraph_key(self,
                          scenario: Scenario,
                          *args) -> str:  # type: ignore
        """Returns the key to be used in shared_data on the subgraph"""

        return f"ribs_in_size_adopting" # noqa E509


class RibsInSizeNonAdoptingSubgraph(RibsInSizeSubgraph):
    """A graph for average number of announcements in the Adj RIBs In for
    adopting ASes.
    """

    name: str = "ribs_in_size_non_adopting"

    def _get_subgraph_key(self,
                          scenario: Scenario,
                          *args) -> str:  # type: ignore
        """Returns the key to be used in shared_data on the subgraph"""

        return f"ribs_in_size_non_adopting" # noqa E509


class RibsInValidNonAdoptingSubgraph(RibsInSizeSubgraph):
    """A graph for average number of announcements in the Adj RIBs In for
    adopting ASes.
    """

    name: str = "ribs_in_valid_non_adopting"

    def _get_subgraph_key(self,
                          scenario: Scenario,
                          *args) -> str:  # type: ignore
        """Returns the key to be used in shared_data on the subgraph"""

        return f"ribs_in_valid_non_adopting" # noqa E509


class RibsInValidAdoptingSubgraph(RibsInSizeSubgraph):
    """A graph for average number of announcements in the Adj RIBs In for
    adopting ASes.
    """

    name: str = "ribs_in_valid_adopting"

    def _get_subgraph_key(self,
                          scenario: Scenario,
                          *args) -> str:  # type: ignore
        """Returns the key to be used in shared_data on the subgraph"""
        return f"ribs_in_valid_adopting" # noqa E509
