from pathlib import Path

from bgpy import Simulation, BGPAS
from bgpy import Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario
from bgpy import AttackerSuccessAdoptingEtcSubgraph
from bgpy import AttackerSuccessAdoptingInputCliqueSubgraph
from bgpy import AttackerSuccessAdoptingStubsAndMHSubgraph
from bgpy import AttackerSuccessNonAdoptingEtcSubgraph
from bgpy import AttackerSuccessNonAdoptingInputCliqueSubgraph
from bgpy import AttackerSuccessNonAdoptingStubsAndMHSubgraph
from bgpy import AttackerSuccessAllSubgraph

from bgp_simulator_pathsec_policies import Aggregator, BGPsecAggressiveAS, BGPsecTransitiveAggressiveAS, BGPsecTransitiveDownOnlyAggressiveAS, BGPsecTransitiveTimidAS, BGPsecTransitiveDownOnlyTimidAS, BGPsecTransitiveDownOnlyNoHashTimidAS, BGPsecTransitiveDownOnlyNoHashAggressiveAS, BGPsecTimidAS, BGPsecTransitiveDownOnlyTimidLeakAS

from bgp_simulator_pathsec_policies import PathManipulationAnn


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
                 parse_cpus=21)
sim.run()
