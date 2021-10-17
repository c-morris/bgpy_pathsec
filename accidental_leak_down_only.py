from pathlib import Path

from lib_bgp_simulator import Simulator, Graph, BGPAS, BGPRIBsAS
from lib_bgp_simulator import Attack, Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario

from bgp_simulator_policies import AccidentalLeak, LeakGraph, DOAnn, DownOnlyAS

from lib_bgp_simulator import Simulator, Graph, ROVAS, SubprefixHijack, BGPAS

graphs = [LeakGraph(
                percent_adoptions=[0, 5, 10, 20, 50, 80, 100],
                adopt_as_classes=[BGPRIBsAS, DownOnlyAS],
                AttackCls=AccidentalLeak,
                num_trials=20,
                propagation_rounds=2,
                base_as_cls=BGPRIBsAS)]
Simulator().run(graphs=graphs, graph_path=Path("/tmp/ezgraphs.tar.gz"))

# Dealing with output data (not in the code yet)
for graph in graphs:
    for data_point, list_of_scenarios in graph.data_points.items():
        print("Percent adoption", data_point.percent_adoption)
        print("Adopted policy:", data_point.ASCls.name)
        print("Propagation round", data_point.propagation_round)
        for scenario in list_of_scenarios:
            from pprint import pprint
            pprint(scenario.data)


