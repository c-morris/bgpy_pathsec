from pathlib import Path

from lib_bgp_simulator import Simulator, Graph, BGPAS, BGPRIBsAS
from lib_bgp_simulator import Attack, Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario

from bgp_simulator_policies import AccidentalLeak, LeakGraph, DOAnn, DownOnlyAS

from lib_bgp_simulator import Simulator, Graph, ROVAS, SubprefixHijack, BGPAS

graphs = [LeakGraph(
                percent_adoptions=[0, 5, 10, 20, 50, 80, 100],
                adopt_as_classes=[BGPRIBsAS, DownOnlyAS],
                AttackCls=AccidentalLeak,
                num_trials=100,
                propagation_rounds=2,
                base_as_cls=BGPRIBsAS)]
Simulator().run(graphs=graphs, graph_path=Path("/tmp/ezgraphs.tar.gz"))

