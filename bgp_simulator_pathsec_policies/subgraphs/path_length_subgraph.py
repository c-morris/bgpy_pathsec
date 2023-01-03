from bgp_simulator_pkg import Subgraph
from bgp_simulator_pkg import Scenario


class PathLengthSubgraph(Subgraph):
    """A graph for average AS path length for ASes"""

    name: str = "path_len_all"

    def _get_subgraph_key(self,
                          scenario: Scenario,
                          *args) -> str:  # type: ignore
        """Returns the key to be used in shared_data on the subgraph"""

        return f"path_len_all" # noqa E509

    @property
    def y_axis_label(self) -> str:
        """returns y axis label"""

        return "Avg AS path length"
