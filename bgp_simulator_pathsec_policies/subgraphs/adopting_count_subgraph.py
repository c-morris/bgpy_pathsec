from bgp_simulator_pkg import Subgraph
from bgp_simulator_pkg import Scenario
from bgp_simulator_pkg import SimulationEngine
from typing import Any, Dict


class AdoptingCountSubgraph(Subgraph):
    """A graph for showing the number of adopting ASes"""

    name: str = "adopting_count"

    def _get_subgraph_key(self,
                          scenario: Scenario,
                          *args) -> str:  # type: ignore
        """Returns the key to be used in shared_data on the subgraph"""

        return f"adopting_count" # noqa E509

    @property
    def y_axis_label(self) -> str:
        """returns y axis label"""

        return "Number of Adopting ASes"
