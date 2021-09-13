from lib_bgp_simulator import Simulator, Graph, BGPPolicy
from lib_bgp_simulator import Attack, Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario

from bgp_simulator_policies import IntentionalLeak, DOAnn

graphs = [Graph(percent_adoptions=[0, 5],
                adopt_policies=[BGPPolicy], # change to DO policy
                AttackCls=IntentionalLeak,
                num_trials=1,
                propagation_rounds=2,
                base_policy=BGPPolicy)]
Simulator().run(graphs=graphs)

# Dealing with output data (not in the code yet)
for graph in graphs:
    for data_point, list_of_scenarios in graph.data_points.items():
        print("Percent adoption", data_point.percent_adoption)
        print("Adopted policy:", data_point.PolicyCls.name)
        print("Propagation round", data_point.propagation_round)
        for scenario in list_of_scenarios:
            print(scenario.data)


