import os
from pathlib import Path

from bgpy import Simulation, BGPAS
from bgpy import Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario

from bgp_simulator_pathsec_policies import Aggregator, PathEndAS, BGPsecAggressiveAS, BGPsecTransitiveAggressiveAS, BGPsecTransitiveDownOnlyAggressiveAS, BGPsecTransitiveTimidAS, BGPsecTransitiveDownOnlyTimidAS, BGPsecTransitiveDownOnlyNoHashTimidAS, BGPsecTransitiveDownOnlyNoHashAggressiveAS, BGPsecTimidAS, BGPsecTransitiveDownOnlyTimidLeakAS, OriginHijack, IntentionalLeak, IntentionalLeakNoHash, BGPsecAS, BGPsecTransitiveAS, BGPsecTransitiveDownOnlyAS, ShortestPathExportAllNoHash, ShortestPathExportAllNoHashUp, TwoHopAttack, IntentionalLeakNoHashUp, RISEavesdropperUp

from bgp_simulator_pathsec_policies import PathManipulationAnn


sim = Simulation(num_trials=50,
                 scenarios=[RISEavesdropperUp(AnnCls=PathManipulationAnn, 
                                              AdoptASCls=BGPsecTransitiveDownOnlyTimidAS,
                                              BaseASCls=BGPAS),
                            ShortestPathExportAllNoHashUp(AnnCls=PathManipulationAnn, 
                                                          AdoptASCls=BGPsecTransitiveDownOnlyAggressiveAS,
                                                          BaseASCls=BGPAS),
                            ],
                 propagation_rounds=2,
                 percent_adoptions=[0.01, 0.1, 0.2, 0.3, 0.5, 0.8, 0.99],
                 output_path=Path(f"/data/ezgraphs{ os.environ['JOB_COMPLETION_INDEX'] }"),
                 parse_cpus=1)
sim.run()
