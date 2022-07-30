from pathlib import Path

from lib_bgp_simulator import Simulation, BGPAS
from lib_bgp_simulator import Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario

from bgp_simulator_policies import Aggregator, BGPsecAggressiveAS, BGPsecTransitiveAggressiveAS, BGPsecTransitiveDownOnlyAggressiveAS, BGPsecTransitiveTimidAS, BGPsecTransitiveDownOnlyTimidAS, BGPsecTransitiveDownOnlyNoHashTimidAS, BGPsecTransitiveDownOnlyNoHashAggressiveAS, BGPsecTimidAS, BGPsecTransitiveDownOnlyTimidLeakAS

from bgp_simulator_policies import PathManipulationAnn


#graphs = [LeakGraph(
#                percent_adoptions=[0.01, 0.1, 0.2, 0.3, 0.5, 0.8, 0.99],
#                adopt_as_classes=[BGPAS, BGPsecAggressiveAS, BGPsecTimidAS, BGPsecTransitiveAggressiveAS, BGPsecTransitiveDownOnlyAggressiveAS, BGPsecTransitiveTimidAS, BGPsecTransitiveDownOnlyTimidAS, BGPsecTransitiveDownOnlyNoHashTimidAS, BGPsecTransitiveDownOnlyNoHashAggressiveAS, BGPsecTransitiveDownOnlyTimidLeakAS], 
#                #adopt_as_classes=[BGPsecTransitiveDownOnlyTimidAS, BGPsecTransitiveDownOnlyNoHashTimidAS], 
#                EngineInputCls=Aggregator,
#                #num_trials=6500,
#                num_trials=2,
#                propagation_rounds=2,
#                BaseASCls=BGPAS)]
#Simulator(parse_cpus=2).run(graphs=graphs, graph_path=Path("/tmp/ezgraphs.tar.gz"))
##Simulator().run(graphs=graphs, graph_path=Path("/tmp/ezgraphs.tar.gz"), mp_method=MPMethod.SINGLE_PROCESS)


sim = Simulation(num_trials=2,
                 scenarios=[Aggregator(AnnCls=PathManipulationAnn, 
                                           AdoptASCls=BGPsecAggressiveAS,
                                           BaseASCls=BGPAS),
                            Aggregator(AnnCls=PathManipulationAnn, 
                                           AdoptASCls=BGPsecTimidAS,
                                           BaseASCls=BGPAS),
                            Aggregator(AnnCls=PathManipulationAnn, 
                                           AdoptASCls=BGPsecTransitiveAggressiveAS,
                                           BaseASCls=BGPAS),
                            Aggregator(AnnCls=PathManipulationAnn, 
                                           AdoptASCls=BGPsecTransitiveTimidAS,
                                           BaseASCls=BGPAS),
                            Aggregator(AnnCls=PathManipulationAnn, 
                                           AdoptASCls=BGPsecTransitiveDownOnlyAggressiveAS,
                                           BaseASCls=BGPAS),
                            Aggregator(AnnCls=PathManipulationAnn, 
                                           AdoptASCls=BGPsecTransitiveDownOnlyTimidAS,
                                           BaseASCls=BGPAS),
                            Aggregator(AnnCls=PathManipulationAnn, 
                                           AdoptASCls=BGPsecTransitiveDownOnlyNoHashAggressiveAS,
                                           BaseASCls=BGPAS),
                            Aggregator(AnnCls=PathManipulationAnn, 
                                           AdoptASCls=BGPsecTransitiveDownOnlyNoHashTimidAS,
                                           BaseASCls=BGPAS),
                            Aggregator(AnnCls=PathManipulationAnn, 
                                           AdoptASCls=BGPsecTransitiveDownOnlyTimidLeakAS,
                                           BaseASCls=BGPAS),
                            ],
                 propagation_rounds=2,
                 percent_adoptions=[0.01, 0.1, 0.2, 0.3, 0.5, 0.8, 0.99],
                 output_path=Path("/tmp/ezgraphs.tar.gz"),
                 parse_cpus=2)
sim.run()
