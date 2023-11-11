Please convert code I'm about to give you from the old way to the new way. I've given an example of the old way below, and also an example of the new way below, respectively.

please do not instantiate the graph, in the new way it comes already instantiated. Additionally, please call it config_p_001 instead of config_001. Please make this changes for all graphs as well.

```
# Old way
from ..graphs import PGraph001
from ....attacks import IntentionalLeak
from ....policies import BGPsecAS
from ....announcements import PathManipulationAnn
from bgpy import EngineTestConfig, BGPAS, ASNs


class Config001(EngineTestConfig):
    """Contains config options to run a test"""

    name = "P001"
    desc = (
        "BGPsec security third preference test, "
        "AS 1 should prefer the path via AS 3"
    )
    scenario = IntentionalLeak(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        BaseASCls=BGPAS,
        AnnCls=PathManipulationAnn,
    )
    graph = PGraph001()
    non_default_as_cls_dict = {
        1: BGPsecAS,
        3: BGPsecAS,
        4: BGPsecAS,
        777: BGPsecAS,
    }
    propagation_rounds = 1
```

```
# New way
from bgpy import EngineTestConfig, BGPAS, ASNs
from bgpy.simulation_framework import ScenarioConfig
from frozendict import frozendict

from ..graphs import p_graph_001
from ....attacks import IntentionalLeak
from ....policies import BGPsecAS
from ....announcements import PathManipulationAnn


config_p_001 = EngineTestConfig(
    name="P001",
    desc = (
        "BGPsec security third preference test, "
        "AS 1 should prefer the path via AS 3"
    )
    scenario_config=ScenarioConfig(
        ScenarioCls=IntentionalLeak,
        AnnCls=PathManipulationAnn,
        BaseASCls=BGPAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({
            1: BGPsecAS,
            3: BGPsecAS,
            4: BGPsecAS,
            777: BGPsecAS,
        }),
    ),
    graph=graph_001,
    propagation_rounds=1,
)
```
