import os
from pathlib import Path

from bgpy import Simulation, BGPAS
from bgpy import Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario, AttackerSuccessAllSubgraph

from bgp_simulator_pathsec_policies import Aggregator, PathEndAS, BGPsecAggressiveAS, BGPsecTransitiveAggressiveAS, BGPsecTransitiveDownOnlyAggressiveAS, BGPsecTransitiveTimidAS, BGPsecTransitiveDownOnlyTimidAS, BGPsecTransitiveDownOnlyNoHashTimidAS, BGPsecTransitiveDownOnlyNoHashAggressiveAS, BGPsecTimidAS, BGPsecTransitiveDownOnlyTimidLeakAS, OriginHijack, IntentionalLeak, IntentionalLeakNoHash, BGPsecAS, BGPsecTransitiveAS, BGPsecTransitiveDownOnlyAS, ShortestPathExportAllNoHash, TwoHopAttack, IntentionalLeakNoHashUp, OverheadAllSubgraph, OverheadBPOAllSubgraph, AdoptingCountSubgraph, NonAdoptingCountSubgraph

from bgp_simulator_pathsec_policies import PathManipulationAnn


sim = Simulation(num_trials=1,
                 scenarios=[
                            OriginHijack(AnnCls=PathManipulationAnn, 
                                         AdoptASCls=BGPsecAS,
                                         BaseASCls=BGPAS),
                            OriginHijack(AnnCls=PathManipulationAnn, 
                                         AdoptASCls=BGPsecTransitiveDownOnlyAS,
                                         BaseASCls=BGPAS),
                            ],
                 propagation_rounds=1,
                 subgraphs=[
                   OverheadBPOAllSubgraph(),
                   OverheadAllSubgraph(),
                   AdoptingCountSubgraph(),
                   NonAdoptingCountSubgraph(),
                   AttackerSuccessAllSubgraph(),
                 ],
                 #percent_adoptions=[0.01, 0.1, 0.2, 0.3, 0.5, 0.8, 0.99, 1.0],
                 percent_adoptions=[1.0],
                 #output_path=Path(f"/data/ezgraphs{ os.environ['JOB_COMPLETION_INDEX'] }"),
                 output_path=Path(f"/tmp/ezgraphs{ os.environ['JOB_COMPLETION_INDEX'] }"),
                 parse_cpus=1)
sim.run()
