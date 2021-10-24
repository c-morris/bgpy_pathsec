from pathlib import Path

from lib_bgp_simulator import Simulator, Graph, BGPSimpleAS, BGPAS
#from lib_bgp_simulator import Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario

from bgp_simulator_policies import AccidentalLeak, LeakGraph, DOAnn, DownOnlyAS

from lib_bgp_simulator import Simulator, Graph, ROVAS, SubprefixHijack, BGPSimpleAS, MPMethod

graphs = [LeakGraph(percent_adoptions=[0, 5, 10, 20, 50, 80, 100],
                    adopt_as_classes=[BGPAS, DownOnlyAS],
                    EngineInputCls=AccidentalLeak,
                    num_trials=100,
                    propagation_rounds=2,
                    BaseASCls=BGPAS)]
Simulator().run(graphs=graphs, graph_path=Path("/tmp/ezgraphs.tar.gz"), mp_method=MPMethod.MP)
