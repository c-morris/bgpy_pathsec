from pathlib import Path

from bgp_simulator_pkg import Simulator, Graph, BGPAS
from bgp_simulator_pkg import Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario

from bgp_simulator_policies import OriginHijack, LeakGraph, DownOnlyAS, BGPsecTransitiveAS, BGPsecAS, BGPsecTransitiveDownOnlyAS

from bgp_simulator_pkg import Simulator, Graph, ROVAS, SubprefixHijack, BGPAS, MPMethod

graphs = [LeakGraph(percent_adoptions=[1, 10, 20, 50, 80, 99],
                    adopt_as_classes=[BGPAS, BGPsecAS, BGPsecTransitiveAS, BGPsecTransitiveDownOnlyAS],
                    EngineInputCls=OriginHijack,
                    num_trials=1,
                    propagation_rounds=1,
                    BaseASCls=BGPAS)]
Simulator().run(graphs=graphs, graph_path=Path("/tmp/test_ezgraphs.tar.gz"), mp_method=MPMethod.MP)
