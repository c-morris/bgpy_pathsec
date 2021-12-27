from pathlib import Path

from lib_bgp_simulator import BGPAS
from lib_bgp_simulator import BaseGraphSystemTester

from bgp_simulator_policies import BGPsecAS, BGPsecTransitiveAS
from bgp_simulator_policies import BGPsecTransitiveDownOnlyAS, IntentionalLeak
from ..graphs import PGraph005


class Test005BGPsecPreference(BaseGraphSystemTester):
    GraphInfoCls = PGraph005
    EngineInputCls = IntentionalLeak
    base_dir = Path(__file__).parent
    BaseASCls = BGPAS
    AdoptASCls = BGPsecAS
    adopting_asns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 777]


class Test005BGPsecTransitivePreference(BaseGraphSystemTester):
    GraphInfoCls = PGraph005
    EngineInputCls = IntentionalLeak
    base_dir = Path(__file__).parent
    BaseASCls = BGPAS
    AdoptASCls = BGPsecTransitiveAS
    adopting_asns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 777]


class Test005BGPsecTransitiveDownOnlyPreference(BaseGraphSystemTester):
    GraphInfoCls = PGraph005
    EngineInputCls = IntentionalLeak
    base_dir = Path(__file__).parent
    BaseASCls = BGPAS
    AdoptASCls = BGPsecTransitiveDownOnlyAS
    adopting_asns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 777]
