from pathlib import Path

from lib_bgp_simulator import BGPAS
from lib_bgp_simulator import BaseGraphSystemTester

from bgp_simulator_policies import DownOnlyAS, BGPsecTransitiveDownOnlyAS
from bgp_simulator_policies import IntentionalLeak
from ..graphs import PGraph003


class Test001DownOnly(BaseGraphSystemTester):
    GraphInfoCls = PGraph003
    EngineInputCls = IntentionalLeak
    base_dir = Path(__file__).parent
    BaseASCls = BGPAS
    AdoptASCls = DownOnlyAS
    adopting_asns = [1, 2, 3, 4, 777]


class Test002DownOnly(BaseGraphSystemTester):
    GraphInfoCls = PGraph003
    EngineInputCls = IntentionalLeak
    base_dir = Path(__file__).parent
    BaseASCls = BGPAS
    AdoptASCls = BGPsecTransitiveDownOnlyAS
    adopting_asns = [1, 2, 3, 4, 777]
