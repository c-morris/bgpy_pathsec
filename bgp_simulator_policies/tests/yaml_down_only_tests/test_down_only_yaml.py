import pytest
from pathlib import Path

from lib_caida_collector import PeerLink, CustomerProviderLink as CPLink
from lib_bgp_simulator import Relationships, BGPAS, Relationships, LocalRIB
from lib_bgp_simulator import ASNs, BaseGraphSystemTester, YamlSystemTestRunner

from bgp_simulator_policies import PTestAnn, DownOnlyAS, BGPsecAS, BGPsecTransitiveAS, BGPsecTransitiveDownOnlyAS, IntentionalLeak
from ..graphs import PGraph003


class Test003DownOnly(BaseGraphSystemTester):
    GraphInfoCls = PGraph003
    EngineInputCls = IntentionalLeak
    base_dir = Path(__file__).parent
    BaseASCls = BGPAS
    AdoptASCls = DownOnlyAS
    adopting_asns = [1, 2, 3, 4, 777]

class Test003DownOnly(BaseGraphSystemTester):
    GraphInfoCls = PGraph003
    EngineInputCls = IntentionalLeak
    base_dir = Path(__file__).parent
    BaseASCls = BGPAS
    AdoptASCls = BGPsecTransitiveDownOnlyAS
    adopting_asns = [1, 2, 3, 4, 777]

