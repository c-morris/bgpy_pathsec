from dataclasses import dataclass

@dataclass(frozen=True)
class PathsecScenarioConfig(ScenarioConfig):
    global_eavesdropper: bool = True
    no_hash: bool = True
    communitites_up: bool = True
    unknown_adopter: bool = False
    attacker_subcategory_attr: str = ASGroups.MULTIHOMED.value
    victim_subcategory_attr: str = ASGroups.MULTIHOMED.value
    transitive_dropping_percent = 0
