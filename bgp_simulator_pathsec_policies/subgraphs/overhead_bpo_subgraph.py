from bgpy import Subgraph
from bgpy import Scenario
from bgpy import SimulationEngine
from typing import Any, Dict


class OverheadBPOAllSubgraph(Subgraph):
    """A graph for average number of signatures verified for all ASes.
    This signature count uses the BPO optimization.
    Values for other subgraphs are also computed here.
    """

    name: str = "overhead_bpo_all"

    def _add_traceback_to_shared_data(self,
                                      shared: Dict[Any, Any],
                                      engine: SimulationEngine,
                                      scenario: Scenario,
                                      outcomes):
        """Adds traceback info to shared data

        All the statistics for all the subgraphs need to be computed here. This
        is because the _add_traceback_to_shared_data function is only called
        for the *first* subgraph class specified in the simulation. The rest
        use the shared_data structure set by the first subgraph.
        """

        uncountable_asns = scenario._preset_asns
        total_path_len = 0
        n_path_len = 0
        total_non_adopting = 0
        total_adopting = 0
        n_ases = 0
        ribs_in_total = 0
        adopting_ribs_in_valid = 0
        non_adopting_ribs_in_valid = 0

        # Set overhead results before checking valid announcements
        bpo_count = engine.as_dict[list(
                scenario.victim_asns)[0]].bpo_count
        overhead_count = engine.as_dict[list(
                scenario.victim_asns)[0]].count
        # Set the number of adopting ASes that were converted to non-adopting
        attacker_as = engine.as_dict[list(scenario.attacker_asns)[0]]
        transitive_dropping_conversions_count = 0
        if hasattr(attacker_as, "convert_count"):
            transitive_dropping_conversions_count = \
                attacker_as.convert_count
        shared["transitive_dropping_conversions_all"] = \
            transitive_dropping_conversions_count

        for as_obj, outcome in outcomes.items():
            if as_obj.asn in uncountable_asns:
                continue
            ribs_in = list(as_obj._ribs_in.get_ann_infos(
                scenario.announcements[0].prefix))
            ribs_in_total += len(ribs_in)
            ribs_in_valid = 0
            ribs_in_invalid = 0
            for ann_info in ribs_in:
                if ann_info.unprocessed_ann is not None:
                    if as_obj._valid_ann(ann_info.unprocessed_ann,
                                         ann_info.recv_relationship):
                        ribs_in_valid += 1
                    else:
                        ribs_in_invalid += 1
            if (as_obj.name == scenario.AdoptASCls.name or
                    as_obj.name == "Pseudo" + scenario.AdoptASCls.name):
                # use of 'in' here because of pseudo adopt AS class
                total_adopting += 1
                adopting_ribs_in_valid += ribs_in_valid
            else:
                total_non_adopting += 1
                non_adopting_ribs_in_valid += ribs_in_valid
            ribs_in_valid = 0
            ribs_in_invalid = 0
            # Check AS path length
            most_specific_ann = self._get_most_specific_ann(
                as_obj, scenario.ordered_prefix_subprefix_dict)
            if most_specific_ann is not None:
                total_path_len += len(most_specific_ann.as_path)
                n_path_len += 1

        n_ases = total_adopting + total_non_adopting

        shared["adopting_count"] = total_adopting
        shared["non_adopting_count"] = total_non_adopting
        if total_adopting != 0:
            shared["overhead_bpo_all"] = bpo_count / total_adopting
            shared["overhead_all"] = overhead_count / total_adopting
            shared["ribs_in_valid_adopting"] = \
                adopting_ribs_in_valid / total_adopting
        if total_non_adopting != 0:
            shared["ribs_in_valid_non_adopting"] = \
                non_adopting_ribs_in_valid / total_non_adopting
        if n_ases != 0:
            shared["ribs_in_size_all"] = ribs_in_total / n_ases
        if total_path_len != 0:
            shared["path_len_all"] = total_path_len / n_path_len
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
