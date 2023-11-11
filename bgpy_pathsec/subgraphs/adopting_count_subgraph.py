from bgpy import Subgraph
from bgpy import Scenario


class AdoptingCountSubgraph(Subgraph):
    """A graph for showing the number of adopting ASes"""

    name: str = "adopting_count"

    def _get_subgraph_key(self, scenario: Scenario, *args) -> str:  # type: ignore
        """Returns the key to be used in shared_data on the subgraph"""

        return f"adopting_count"

    @property
    def y_axis_label(self) -> str:
        """returns y axis label"""

        return "Number of Adopting ASes"
