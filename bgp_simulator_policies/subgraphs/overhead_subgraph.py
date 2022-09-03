from bgp_simulator_pkg import Subgraph
from bgp_simulator_pkg import Outcomes
from bgp_simulator_pkg import Scenario
from bgp_simulator_pkg import SimulationEngine
from typing import Any, Dict

from ..policies import BGPsecAS


class OverheadAllSubgraph(Subgraph):
    """A graph for attacker success for all ASes"""

    name: str = "overhead_all"

    def _add_traceback_to_shared_data(self,
                                      shared: Dict[Any, Any],
                                      engine: SimulationEngine,
                                      scenario: Scenario,
                                      outcomes):
        """Adds traceback info to shared data"""

        #shared["all_overhead"] = engine.as_dict[list(scenario.victim_asns)[0]].total_signature_verifications
        #shared["all_overhead"] = BGPsecAS.count
        shared["overhead_all"] = engine.as_dict[list(scenario.victim_asns)[0]].count
        #BGPsecAS.count = 0
        #print('\naa', engine.as_dict[list(scenario.victim_asns)[0]].count)
        #engine.as_dict[list(scenario.victim_asns)[0]].total_signature_verifications = 0
        return super()._add_traceback_to_shared_data(shared, engine, scenario, outcomes)

    def _get_subgraph_key(self,
                          scenario: Scenario,
                          *args) -> str:  # type: ignore
        """Returns the key to be used in shared_data on the subgraph"""

        return f"overhead_all" # noqa E509

    @property
    def y_axis_label(self) -> str:
        """returns y axis label"""

        return "Total signatures verified"
