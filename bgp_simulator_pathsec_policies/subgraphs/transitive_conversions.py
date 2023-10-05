from bgpy import Subgraph
from bgpy import Scenario


class TransitiveDroppingConversionsAllSubgraph(Subgraph):
    """A graph for average number of signatures verified for all ASes"""

    name: str = "transitive_dropping_conversions_all"

    def _get_subgraph_key(self,
                          scenario: Scenario,
                          *args) -> str:  # type: ignore
        """Returns the key to be used in shared_data on the subgraph"""

        return f"transitive_dropping_conversions_all" # noqa E509

    @property
    def y_axis_label(self) -> str:
        """returns y axis label"""

        return "Number of Adopting ASes with Transitive Dropping Providers"
