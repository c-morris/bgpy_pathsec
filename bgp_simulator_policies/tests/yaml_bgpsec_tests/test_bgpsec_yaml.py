from pathlib import Path

from lib_bgp_simulator import BGPAS
from lib_bgp_simulator import BaseGraphSystemTester

from bgp_simulator_policies import BGPsecAS, BGPsecTransitiveAS
from bgp_simulator_policies import BGPsecTransitiveDownOnlyAS, IntentionalLeak
from ..graphs import PGraph001


class Test001BGPsecPreference(BaseGraphSystemTester):
    GraphInfoCls = PGraph001
    EngineInputCls = IntentionalLeak
    base_dir = Path(__file__).parent
    BaseASCls = BGPAS
    AdoptASCls = BGPsecAS
    adopting_asns = [1, 3, 4, 777]


class Test001BGPsecTransitivePreference(BaseGraphSystemTester):
    GraphInfoCls = PGraph001
    EngineInputCls = IntentionalLeak
    base_dir = Path(__file__).parent
    BaseASCls = BGPAS
    AdoptASCls = BGPsecTransitiveAS
    adopting_asns = [1, 3, 4, 777]


class Test001BGPsecTransitiveDownOnlyPreference(BaseGraphSystemTester):
    GraphInfoCls = PGraph001
    EngineInputCls = IntentionalLeak
    base_dir = Path(__file__).parent
    BaseASCls = BGPAS
    AdoptASCls = BGPsecTransitiveDownOnlyAS
    adopting_asns = [1, 3, 4, 777]
