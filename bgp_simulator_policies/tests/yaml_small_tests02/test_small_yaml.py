from pathlib import Path

from lib_bgp_simulator import BGPAS
from lib_bgp_simulator import BaseGraphSystemTester

from bgp_simulator_policies import BGPsecAS, BGPsecTransitiveAS
from bgp_simulator_policies import BGPsecTransitiveDownOnlyAS, IntentionalLeak
from ..graphs import PGraph006


class Test006BGPsecPreference(BaseGraphSystemTester):
    GraphInfoCls = PGraph006
    EngineInputCls = IntentionalLeak
    base_dir = Path(__file__).parent
    BaseASCls = BGPAS
    AdoptASCls = BGPsecAS
    adopting_asns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 777]


class Test006BGPsecTransitivePreference(BaseGraphSystemTester):
    GraphInfoCls = PGraph006
    EngineInputCls = IntentionalLeak
    base_dir = Path(__file__).parent
    BaseASCls = BGPAS
    AdoptASCls = BGPsecTransitiveAS
    adopting_asns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 777]


class Test006BGPsecTransitiveDownOnlyPreference(BaseGraphSystemTester):
    GraphInfoCls = PGraph006
    EngineInputCls = IntentionalLeak
    base_dir = Path(__file__).parent
    BaseASCls = BGPAS
    AdoptASCls = BGPsecTransitiveDownOnlyAS
    adopting_asns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 777]
