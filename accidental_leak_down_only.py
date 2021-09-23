from lib_bgp_simulator import Simulator, Graph, BGPPolicy, BGPRIBSPolicy
from lib_bgp_simulator import Attack, Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario

from bgp_simulator_policies import AccidentalLeak, LeakGraph, DOAnn, DownOnlyPolicy

from lib_bgp_simulator import Simulator, Graph, ROVPolicy, SubprefixHijack, BGPPolicy

graphs = [LeakGraph(
                percent_adoptions=[0, 10, 20, 50, 80, 100],
                adopt_policies=[BGPRIBSPolicy, DownOnlyPolicy],
                AttackCls=AccidentalLeak,
                num_trials=2,
                propagation_rounds=2,
                base_policy=BGPRIBSPolicy)]
Simulator().run(graphs=graphs, graph_path="/home/cbm14007/Downloads/graphs/graphs.tar.gz")

# Dealing with output data (not in the code yet)
for graph in graphs:
    for data_point, list_of_scenarios in graph.data_points.items():
        print("Percent adoption", data_point.percent_adoption)
        print("Adopted policy:", data_point.PolicyCls.name)
        print("Propagation round", data_point.propagation_round)
        for scenario in list_of_scenarios:
            print(scenario.data)


