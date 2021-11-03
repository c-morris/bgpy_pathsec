import pytest
from pathlib import Path

from lib_caida_collector import PeerLink, CustomerProviderLink as CPLink
from lib_bgp_simulator import Relationships, BGPAS, Relationships, LocalRIB
from lib_bgp_simulator import ASNs, BaseGraphSystemTester, YamlSystemTestRunner

from bgp_simulator_policies import PTestAnn, DownOnlyAS, BGPsecAS, BGPsecTransitiveAS, BGPsecTransitiveDownOnlyAS, IntentionalLeak
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

