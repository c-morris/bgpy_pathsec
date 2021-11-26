from pathlib import Path

from lib_bgp_simulator import Simulator, Graph, BGPAS
from lib_bgp_simulator import Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario

from bgp_simulator_policies import IntentionalLeak, LeakGraph, PAnn, DownOnlyAS, BGPsecTransitiveAS, BGPsecAS, BGPsecTransitiveDownOnlyAS

from lib_bgp_simulator import Simulator, Graph, ROVAS, SubprefixHijack, BGPAS, MPMethod

graphs = [LeakGraph(
                #percent_adoptions=[1, 10, 20, 50, 80, 99],
                #percent_adoptions=[80, 99],
                percent_adoptions=[100],
                adopt_as_classes=[BGPAS, BGPsecTransitiveAS, BGPsecTransitiveDownOnlyAS], 
                EngineInputCls=IntentionalLeak,
                num_trials=3000,
                propagation_rounds=2,
                BaseASCls=BGPAS)]
Simulator().run(graphs=graphs, graph_path=Path("/tmp/ezgraphs.tar.gz"), mp_method=MPMethod.MP)

# Dealing with output data (not in the code yet)
#for graph in graphs:
#    for data_point, list_of_scenarios in graph.data_points.items():
#        print("Percent adoption", data_point.percent_adoption)
#        print("Adopted policy:", data_point.ASCls.name)
#        print("Propagation round", data_point.propagation_round)
#        for scenario in list_of_scenarios:
#            print(scenario.data)
#

