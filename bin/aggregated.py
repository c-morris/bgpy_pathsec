from pathlib import Path

from lib_bgp_simulator import Simulation, BGPAS
from lib_bgp_simulator import Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario
from lib_bgp_simulator import AttackerSuccessAdoptingEtcSubgraph
from lib_bgp_simulator import AttackerSuccessAdoptingInputCliqueSubgraph
from lib_bgp_simulator import AttackerSuccessAdoptingStubsAndMHSubgraph
from lib_bgp_simulator import AttackerSuccessNonAdoptingEtcSubgraph
from lib_bgp_simulator import AttackerSuccessNonAdoptingInputCliqueSubgraph
from lib_bgp_simulator import AttackerSuccessNonAdoptingStubsAndMHSubgraph

from bgp_simulator_policies import Aggregator, BGPsecAggressiveAS, BGPsecTransitiveAggressiveAS, BGPsecTransitiveDownOnlyAggressiveAS, BGPsecTransitiveTimidAS, BGPsecTransitiveDownOnlyTimidAS, BGPsecTransitiveDownOnlyNoHashTimidAS, BGPsecTransitiveDownOnlyNoHashAggressiveAS, BGPsecTimidAS, BGPsecTransitiveDownOnlyTimidLeakAS

from bgp_simulator_policies import PathManipulationAnn
from bgp_simulator_policies import AttackerSuccessAllSubgraph


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
                 subgraphs=[
                   AttackerSuccessAllSubgraph(),
                   AttackerSuccessAdoptingEtcSubgraph(),
                   AttackerSuccessAdoptingInputCliqueSubgraph(),
                   AttackerSuccessAdoptingStubsAndMHSubgraph(),
                   AttackerSuccessNonAdoptingEtcSubgraph(),
                   AttackerSuccessNonAdoptingInputCliqueSubgraph(),
                   AttackerSuccessNonAdoptingStubsAndMHSubgraph()],
                 propagation_rounds=2,
                 percent_adoptions=[0.01, 0.1, 0.2, 0.3, 0.5, 0.8, 0.99],
                 output_path=Path("/tmp/ezgraphs"),
                 parse_cpus=2)
sim.run()
