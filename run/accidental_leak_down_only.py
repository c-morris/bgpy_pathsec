from pathlib import Path

from bgp_simulator_pkg import Simulation, BGPSimpleAS, BGPAS

from bgp_simulator_pathsec_policies import AccidentalLeak, PathManipulationAnn, DownOnlyAS

sim = Simulation(num_trials=2,
                 scenarios=[AccidentalLeak(AnnCls=PathManipulationAnn, 
                                           AdoptASCls=DownOnlyAS,
                                           BaseASCls=BGPAS)],
                 propagation_rounds=2,
                 percent_adoptions = (0.01, 0.1, 0.2, 0.4, 0.6, 0.8, 0.99),
                 output_path=Path("/tmp/ezgraphs.tar.gz"),
                 parse_cpus=2)
sim.run()
