from bgp_simulator_pkg import Subgraph
from bgp_simulator_pkg import Scenario
from bgp_simulator_pkg import SimulationEngine
from bgp_simulator_pkg import BGPAS
from typing import Any, Dict


class OverheadBPOAllSubgraph(Subgraph):
    """A graph for attacker success for all ASes"""

    name: str = "overhead_bpo_all"

    def _add_traceback_to_shared_data(self,
                                      shared: Dict[Any, Any],
                                      engine: SimulationEngine,
                                      scenario: Scenario,
                                      outcomes):
        """Adds traceback info to shared data"""

        uncountable_asns = scenario._preset_asns

        total_non_adopting = 0
        for as_obj, outcome in outcomes.items():
            if as_obj.asn in uncountable_asns:
                continue
            if as_obj.__class__ != scenario.AdoptASCls:
                total_non_adopting += 1
        total_adopting = len(outcomes) - total_non_adopting

        shared["overhead_bpo_all"] = engine.as_dict[list(
            scenario.victim_asns)[0]].bpo_count / total_adopting
        shared["overhead_all"] = engine.as_dict[list(
            scenario.victim_asns)[0]].count / total_adopting
        shared["adopting_count"] = total_adopting
        shared["non_adopting_count"] = total_non_adopting
        super()._add_traceback_to_shared_data(
            shared, engine, scenario, outcomes)

    def _get_subgraph_key(self,
                          scenario: Scenario,
                          *args) -> str:  # type: ignore
        """Returns the key to be used in shared_data on the subgraph"""

        return f"overhead_bpo_all" # noqa E509

    @property
    def y_axis_label(self) -> str:
        """returns y axis label"""

        return "Avg signatures verified per AS (BPO)"
