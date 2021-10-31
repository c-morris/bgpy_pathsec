import pytest
from pathlib import Path

from lib_caida_collector import PeerLink, CustomerProviderLink as CPLink
from lib_bgp_simulator import Relationships, BGPAS, Relationships, LocalRIB
from lib_bgp_simulator import ASNs, BaseGraphSystemTester, YamlSystemTestRunner

from bgp_simulator_policies import PTestAnn, DownOnlyAS, BGPsecAS, BGPsecTransitiveAS, BGPsecTransitiveDownOnlyAS, IntentionalLeak
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

class Test001BGPsecPreference(BaseGraphSystemTester):
    GraphInfoCls = PGraph001
    EngineInputCls = IntentionalLeak
    base_dir = Path(__file__).parent
    BaseASCls = BGPAS
    AdoptASCls = BGPsecTransitiveDownOnlyAS
    adopting_asns = [1, 3, 4, 777]

