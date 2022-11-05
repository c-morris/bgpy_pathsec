from bgp_simulator_pkg import Subgraph
from bgp_simulator_pkg import Scenario


class OverheadAllSubgraph(Subgraph):
    """A graph for attacker success for all ASes"""

    name: str = "overhead_all"

    def _get_subgraph_key(self,
                          scenario: Scenario,
                          *args) -> str:  # type: ignore
        """Returns the key to be used in shared_data on the subgraph"""

        return f"overhead_all" # noqa E509

    @property
    def y_axis_label(self) -> str:
        """returns y axis label"""

        return "Avg signatures verified per AS"
