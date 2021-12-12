from pathlib import Path

from lib_bgp_simulator import Simulator, Graph, BGPAS
from lib_bgp_simulator import Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario

from bgp_simulator_policies import IntentionalLeakNoHash, LeakGraph, PAnn, DownOnlyAS, BGPsecTransitiveAS, BGPsecAS, BGPsecTransitiveDownOnlyAS

from lib_bgp_simulator import Simulator, Graph, ROVAS, SubprefixHijack, BGPAS, MPMethod

graphs = [LeakGraph(
                percent_adoptions=[1, 10, 20, 50, 80, 99],
                adopt_as_classes=[BGPAS, BGPsecTransitiveAS, BGPsecTransitiveDownOnlyAS], 
                EngineInputCls=IntentionalLeakNoHash,
                num_trials=1000,
                propagation_rounds=2,
                BaseASCls=BGPAS)]
Simulator().run(graphs=graphs, graph_path=Path("/tmp/ezgraphs.tar.gz"), mp_method=MPMethod.MP)


