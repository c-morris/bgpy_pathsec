from pathlib import Path

from lib_bgp_simulator import BGPAS
from lib_bgp_simulator import BaseGraphSystemTester

from bgp_simulator_policies import BGPsecTransitiveAS
from bgp_simulator_policies import BGPsecTransitiveDownOnlyAS
from bgp_simulator_policies import IntentionalLeak
from ..graphs import PGraph002


class Test001BGPsecTransitivePreference(BaseGraphSystemTester):
    GraphInfoCls = PGraph002
    EngineInputCls = IntentionalLeak
    base_dir = Path(__file__).parent
    BaseASCls = BGPAS
    AdoptASCls = BGPsecTransitiveAS
    adopting_asns = [1, 2, 3, 4, 7, 8, 9, 777]


class Test002BGPsecTransitivePreference(BaseGraphSystemTester):
    GraphInfoCls = PGraph002
    EngineInputCls = IntentionalLeak
    base_dir = Path(__file__).parent
    BaseASCls = BGPAS
    AdoptASCls = BGPsecTransitiveDownOnlyAS
    adopting_asns = [1, 2, 3, 4, 7, 8, 9, 777]
