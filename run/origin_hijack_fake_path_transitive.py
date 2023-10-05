from bgpy import Simulator, Graph, BGPPolicy, BGPRIBSPolicy
from bgpy import Attack, Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario

from bgp_simulator_pathsec_policies import OriginHijack, LeakGraph, PAnn, BGPsecPolicy, BGPsecTransitivePolicy

from bgpy import Simulator, Graph, ROVPolicy, SubprefixHijack, BGPPolicy

graphs = [LeakGraph(
                percent_adoptions=[0, 10, 20, 50, 80, 100],
                adopt_policies=[BGPRIBSPolicy, BGPsecPolicy, BGPsecTransitivePolicy],
                AttackCls=OriginHijack,
                num_trials=200,
                propagation_rounds=1,
                base_policy=BGPRIBSPolicy)]
Simulator().run(graphs=graphs, graph_path="/home/cam/graphs/graphs.tar.gz")

# Dealing with output data (not in the code yet)
#for graph in graphs:
#    for data_point, list_of_scenarios in graph.data_points.items():
#        print("Percent adoption", data_point.percent_adoption)
#        print("Adopted policy:", data_point.PolicyCls.name)
#        print("Propagation round", data_point.propagation_round)
#        for scenario in list_of_scenarios:
#            print(scenario.data)
#
