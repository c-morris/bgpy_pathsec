from typing import Union
from bgpy.bgpy import Scenario
from bgpy.bgpy import MetricTracker
from bgpy.bgpy import Subgraph
from bgpy.bgpy import SimulationEngine
from bgpy.bgpy.enums import SpecialPercentAdoptions

class AdoptingCountMetricTracker(MetricTracker):
    """A metric tracker for showing the number of adopting ASes"""
    
    name: str = "adopting_count"
    
    def _track_trial_metrics_hook(
        self,
        *,
        engine: SimulationEngine,
        percent_adopt: Union[float, SpecialPercentAdoptions],
        trial: int,
        scenario: Scenario,
        propagation_round: int,
        outcomes,
    ) -> None:
        """Hook function for easy subclassing by a user"""

        pass


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
