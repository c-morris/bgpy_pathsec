import os
from pathlib import Path

from bgp_simulator_pkg import Simulation, BGPAS
from bgp_simulator_pkg import Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario, AttackerSuccessAllSubgraph, DisconnectedAllSubgraph, VictimSuccessAllSubgraph

from bgp_simulator_pathsec_policies import Aggregator, PathEndAS, BGPsecAggressiveAS, BGPsecTransitiveAggressiveAS, BGPsecTransitiveDownOnlyAggressiveAS, BGPsecTransitiveTimidAS, BGPsecTransitiveDownOnlyTimidAS, BGPsecTransitiveDownOnlyNoHashTimidAS, BGPsecTransitiveDownOnlyNoHashAggressiveAS, BGPsecTimidAS, BGPsecTransitiveDownOnlyTimidLeakAS, OriginHijack, IntentionalLeak, IntentionalLeakNoHash, BGPsecAS, BGPsecTransitiveAS, BGPsecTransitiveDownOnlyAS, ShortestPathExportAllNoHash, ShortestPathExportAllNoHashUp, TwoHopAttack, IntentionalLeakNoHashUp, RISEavesdropperUp, TwoHopAttack, OverheadAllSubgraph, OverheadBPOAllSubgraph, AdoptingCountSubgraph, NonAdoptingCountSubgraph, ShortestPathExportAll, BGPsecTransitiveDownOnlyNoHashUpTimidAS, PathEndAggressiveAS, PathEndTimidAS

from bgp_simulator_pathsec_policies import PathManipulationAnn

sim = Simulation(
    num_trials=2,
    scenarios=[
        OriginHijack(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=BGPsecAggressiveAS,
            BaseASCls=BGPAS),
        # BGPsec Timid never makes sense, aggressive is always better
        # ShortestPathExportAll(AnnCls=PathManipulationAnn, 
        #                       AdoptASCls=BGPsecTimidAS,
        #                       BaseASCls=BGPAS),
        OriginHijack(
            AnnCls=PathManipulationAnn, 
            # NoHash doesn't matter for aggressive 
            AdoptASCls=BGPsecTransitiveAggressiveAS,
            BaseASCls=BGPAS),
        ShortestPathExportAllNoHash(
            AnnCls=PathManipulationAnn, 
            # All BGPsecTransitive attacks must be NoHash
            AdoptASCls=BGPsecTransitiveTimidAS,
            BaseASCls=BGPAS),
        OriginHijack(
            AnnCls=PathManipulationAnn, 
            # The aggressive case covers both NoHash and Up
            AdoptASCls=BGPsecTransitiveDownOnlyAggressiveAS,
            BaseASCls=BGPAS),
        ShortestPathExportAll(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=BGPsecTransitiveDownOnlyTimidAS,
            BaseASCls=BGPAS),
        ShortestPathExportAllNoHash(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=BGPsecTransitiveDownOnlyNoHashTimidAS,
            BaseASCls=BGPAS),
        # duplicate?
        #ShortestPathExportAllNoHashUp(
        #    AnnCls=PathManipulationAnn, 
        #    AdoptASCls=BGPsecTransitiveDownOnlyNoHashUpTimidAS,
        #    BaseASCls=BGPAS),
        OriginHijack(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=PathEndAggressiveAS,
            BaseASCls=BGPAS),
        TwoHopAttack(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=PathEndTimidAS,
            BaseASCls=BGPAS),
        # NEED TWO HOP UP VARIANT
        # ALSO NEED UP VARIANTS WITHOUT NO HASH (or do we?)
        #IntentionalLeakNoHash(AnnCls=PathManipulationAnn, 
        #               AdoptASCls=BGPsecTransitiveAS,
        #               BaseASCls=BGPAS),
        ],
    propagation_rounds=2,
    subgraphs=[
        OverheadBPOAllSubgraph(),
        OverheadAllSubgraph(),
        AdoptingCountSubgraph(),
        NonAdoptingCountSubgraph(),
        AttackerSuccessAllSubgraph(),
        VictimSuccessAllSubgraph(),
        DisconnectedAllSubgraph()
    ],
    percent_adoptions=[0.01, 0.1, 0.2, 0.3, 0.5, 0.8, 0.99],
    #output_path=Path(f"/data/ezgraphs{ os.environ['JOB_COMPLETION_INDEX'] }"),
    output_path=Path(f"/tmp/ezgraphs{ os.environ['JOB_COMPLETION_INDEX'] }"),
    parse_cpus=2)

sim.run()

