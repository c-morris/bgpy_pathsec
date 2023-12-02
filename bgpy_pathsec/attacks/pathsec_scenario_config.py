from dataclasses import dataclass

from bgpy.simulation_framework import ScenarioConfig
from bgpy.enums import ASGroups


@dataclass(frozen=True)
class PathsecScenarioConfig(ScenarioConfig):
    global_eavesdropper: bool = True
    no_hash: bool = True
    communities_up: bool = True
    unknown_adopter: bool = False
    attacker_subcategory_attr: str = ASGroups.MULTIHOMED.value
    victim_subcategory_attr: str = ASGroups.MULTIHOMED.value
    transitive_dropping_percent: int = 0
