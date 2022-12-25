import os
from pathlib import Path

from bgp_simulator_pkg import Simulation, BGPAS, ValidPrefix
from bgp_simulator_pkg import Prefixes
from bgp_simulator_pkg import Timestamps
from bgp_simulator_pkg import ASNs
from bgp_simulator_pkg import Announcement
from bgp_simulator_pkg import Relationships
from bgp_simulator_pkg import Scenario
from bgp_simulator_pkg import AttackerSuccessAllSubgraph
from bgp_simulator_pkg import DisconnectedAllSubgraph
from bgp_simulator_pkg import VictimSuccessAllSubgraph

from bgp_simulator_pathsec_policies import PathManipulationAnn
from bgp_simulator_pathsec_policies import PathEndAS
from bgp_simulator_pathsec_policies import BGPsecAggressiveAS
from bgp_simulator_pathsec_policies import BGPsecTransitiveAggressiveAS
from bgp_simulator_pathsec_policies import BGPsecTransitiveDownOnlyAggressiveAS
from bgp_simulator_pathsec_policies import BGPsecTransitiveTimidAS
from bgp_simulator_pathsec_policies import BGPsecTransitiveDownOnlyTimidAS
from bgp_simulator_pathsec_policies import BGPsecTransitiveDownOnlyNoHashTimidAS
from bgp_simulator_pathsec_policies import BGPsecTransitiveDownOnlyNoHashAggressiveAS
from bgp_simulator_pathsec_policies import BGPsecTimidAS
from bgp_simulator_pathsec_policies import BGPsecTransitiveDownOnlyTimidLeakAS
from bgp_simulator_pathsec_policies import OriginHijack
from bgp_simulator_pathsec_policies import IntentionalLeak
from bgp_simulator_pathsec_policies import IntentionalLeakNoHash
from bgp_simulator_pathsec_policies import BGPsecAS
from bgp_simulator_pathsec_policies import BGPsecTransitiveAS
from bgp_simulator_pathsec_policies import BGPsecTransitiveDownOnlyAS
from bgp_simulator_pathsec_policies import ShortestPathExportAllNoHash
from bgp_simulator_pathsec_policies import ShortestPathExportAllNoHashUp
from bgp_simulator_pathsec_policies import TwoHopAttack
from bgp_simulator_pathsec_policies import IntentionalLeakNoHashUp
from bgp_simulator_pathsec_policies import RISEavesdropperUp
from bgp_simulator_pathsec_policies import TwoHopAttackUp
from bgp_simulator_pathsec_policies import OverheadAllSubgraph
from bgp_simulator_pathsec_policies import OverheadBPOAllSubgraph
from bgp_simulator_pathsec_policies import AdoptingCountSubgraph
from bgp_simulator_pathsec_policies import NonAdoptingCountSubgraph
from bgp_simulator_pathsec_policies import ShortestPathExportAll
from bgp_simulator_pathsec_policies import BGPsecTransitiveDownOnlyNoHashUpTimidAS
from bgp_simulator_pathsec_policies import PathEndAggressiveAS
from bgp_simulator_pathsec_policies import PathEndTimidAS
from bgp_simulator_pathsec_policies import BaselineBGPAS
from bgp_simulator_pathsec_policies import ShortestPathExportAllNoHashTimid
from bgp_simulator_pathsec_policies import PathEndTimidUpAS
from bgp_simulator_pathsec_policies import ShortestPathExportAllUp
from bgp_simulator_pathsec_policies import BGPsecTransitiveDownOnlyUpTimidAS
from bgp_simulator_pathsec_policies import OverheadBGPsecAS
from bgp_simulator_pathsec_policies import OverheadBGPsecTransitiveDownOnlyAS


sim = Simulation(
    num_trials=15,
    scenarios=[
        OriginHijack(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=BGPsecAggressiveAS,
            BaseASCls=BGPAS),
        # BGPsec Timid never makes sense, aggressive is always better
        # ShortestPathExportAll(
        #     AnnCls=PathManipulationAnn, 
        #     AdoptASCls=BGPsecTimidAS,
        #     BaseASCls=BGPAS),
        OriginHijack(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=BGPsecTransitiveAggressiveAS,
            BaseASCls=BGPAS),
        ShortestPathExportAllNoHash(
            AnnCls=PathManipulationAnn, 
            # All BGPsecTransitive attacks must be NoHash
            AdoptASCls=BGPsecTransitiveTimidAS,
            BaseASCls=BGPAS),
        OriginHijack(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=BGPsecTransitiveDownOnlyAggressiveAS,
            BaseASCls=BGPAS),
        ShortestPathExportAll(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=BGPsecTransitiveDownOnlyTimidAS,
            BaseASCls=BGPAS),
        ShortestPathExportAllUp(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=BGPsecTransitiveDownOnlyUpTimidAS,
            BaseASCls=BGPAS),
        ShortestPathExportAllNoHash(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=BGPsecTransitiveDownOnlyNoHashTimidAS,
            BaseASCls=BGPAS),
        ShortestPathExportAllNoHashUp(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=BGPsecTransitiveDownOnlyNoHashUpTimidAS,
            BaseASCls=BGPAS),
        ShortestPathExportAllNoHashTimid(
            AnnCls=PathManipulationAnn, 
            # This says TimidLeak, it's really NoHashTimidLeak
            AdoptASCls=BGPsecTransitiveDownOnlyTimidLeakAS,
            BaseASCls=BGPAS),
        OriginHijack(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=PathEndAggressiveAS,
            BaseASCls=BGPAS),
        TwoHopAttack(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=PathEndTimidAS,
            BaseASCls=BGPAS),
        TwoHopAttackUp(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=PathEndTimidUpAS,
            BaseASCls=BGPAS),
        OriginHijack(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=BaselineBGPAS,
            BaseASCls=BGPAS),
        ValidPrefix(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=OverheadBGPsecAS,
            BaseASCls=BGPAS),
        ValidPrefix(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=OverheadBGPsecTransitiveDownOnlyAS,
            BaseASCls=BGPAS),
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
    output_path=Path(f"/data/ezgraphs{ os.environ['JOB_COMPLETION_INDEX'] }"),
    #output_path=Path(f"/tmp/ezgraphs{ os.environ['JOB_COMPLETION_INDEX'] }"),
    parse_cpus=1)

sim.run()

