from pathlib import Path

from lib_bgp_simulator import Simulator, Graph, BGPAS
from lib_bgp_simulator import Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario

from bgp_simulator_policies import Aggregator, LeakGraph, PAnn, BGPsecAggressiveAS, BGPsecTransitiveAggressiveAS, BGPsecTransitiveDownOnlyAggressiveAS, BGPsecTransitiveTimidAS, BGPsecTransitiveDownOnlyTimidAS, BGPsecTransitiveDownOnlyNoHashTimidAS 

from lib_bgp_simulator import Simulator, Graph, ROVAS, SubprefixHijack, BGPAS, MPMethod

graphs = [LeakGraph(
                percent_adoptions=[1, 10, 20, 50, 80, 99],
                adopt_as_classes=[BGPAS, BGPsecAggressiveAS, BGPsecTransitiveAggressiveAS, BGPsecTransitiveDownOnlyAggressiveAS, BGPsecTransitiveTimidAS, BGPsecTransitiveDownOnlyTimidAS, BGPsecTransitiveDownOnlyNoHashTimidAS], 
                EngineInputCls=Aggregator,
                num_trials=2,
                propagation_rounds=2,
                BaseASCls=BGPAS)]
Simulator().run(graphs=graphs, graph_path=Path("/tmp/ezgraphs.tar.gz"), mp_method=MPMethod.MP)

