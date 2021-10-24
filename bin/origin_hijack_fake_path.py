from pathlib import Path

from lib_bgp_simulator import Simulator, Graph, BGPAS
from lib_bgp_simulator import Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario

from bgp_simulator_policies import OriginHijack, LeakGraph, PAnn, BGPsecAS

from lib_bgp_simulator import Simulator, Graph, ROVAS, SubprefixHijack, BGPAS

graphs = [LeakGraph(percent_adoptions=[0, 10, 20, 50, 80, 100],
                    adopt_as_classes=[BGPAS, BGPsecAS],
                    EngineInputCls=OriginHijack,
                    num_trials=2,
                    propagation_rounds=1,
                    BaseASCls=BGPAS)]
Simulator().run(graphs=graphs, graph_path=Path("/home/cbm14007/Downloads/graphs/graphs.tar.gz"))
