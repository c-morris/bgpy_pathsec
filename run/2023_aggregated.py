import os
import random
from pathlib import Path

from bgp_simulator_pkg import Simulation, BGPAS
from bgp_simulator_pkg import Prefixes
from bgp_simulator_pkg import Timestamps
from bgp_simulator_pkg import ASNs
from bgp_simulator_pkg import Announcement
from bgp_simulator_pkg import Relationships
from bgp_simulator_pkg import Scenario
from bgp_simulator_pkg import AttackerSuccessAllSubgraph
from bgp_simulator_pkg import DisconnectedAllSubgraph
from bgp_simulator_pkg import VictimSuccessAllSubgraph

from bgp_simulator_pkg import AttackerSuccessAdoptingEtcSubgraph
from bgp_simulator_pkg import AttackerSuccessAdoptingInputCliqueSubgraph
from bgp_simulator_pkg import AttackerSuccessAdoptingStubsAndMHSubgraph
from bgp_simulator_pkg import AttackerSuccessNonAdoptingEtcSubgraph
from bgp_simulator_pkg import AttackerSuccessNonAdoptingInputCliqueSubgraph
from bgp_simulator_pkg import AttackerSuccessNonAdoptingStubsAndMHSubgraph

from bgp_simulator_pkg import DisconnectedAdoptingEtcSubgraph
from bgp_simulator_pkg import DisconnectedAdoptingInputCliqueSubgraph
from bgp_simulator_pkg import DisconnectedAdoptingStubsAndMHSubgraph
from bgp_simulator_pkg import DisconnectedNonAdoptingEtcSubgraph
from bgp_simulator_pkg import DisconnectedNonAdoptingInputCliqueSubgraph
from bgp_simulator_pkg import DisconnectedNonAdoptingStubsAndMHSubgraph

from bgp_simulator_pkg import VictimSuccessAdoptingEtcSubgraph
from bgp_simulator_pkg import VictimSuccessAdoptingInputCliqueSubgraph
from bgp_simulator_pkg import VictimSuccessAdoptingStubsAndMHSubgraph
from bgp_simulator_pkg import VictimSuccessNonAdoptingEtcSubgraph
from bgp_simulator_pkg import VictimSuccessNonAdoptingInputCliqueSubgraph
from bgp_simulator_pkg import VictimSuccessNonAdoptingStubsAndMHSubgraph

from bgp_simulator_pathsec_policies import PathManipulationAnn
from bgp_simulator_pathsec_policies import PathEndAS
from bgp_simulator_pathsec_policies import BGPsecAggressiveAS
from bgp_simulator_pathsec_policies import BGPsecTransitiveAggressiveAS
from bgp_simulator_pathsec_policies import BGPsecTransitiveDownOnlyAggressiveAS
from bgp_simulator_pathsec_policies import BGPsecTransitiveTimidAS
from bgp_simulator_pathsec_policies import BGPsecTransitiveDownOnlyTimidAS
from bgp_simulator_pathsec_policies import BGPsecTransitiveDownOnlyNoHashTimidAS
from bgp_simulator_pathsec_policies import BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping1AS
from bgp_simulator_pathsec_policies import BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping2AS
from bgp_simulator_pathsec_policies import BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping4AS
from bgp_simulator_pathsec_policies import BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping8AS
from bgp_simulator_pathsec_policies import BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping16AS
from bgp_simulator_pathsec_policies import BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping32AS
from bgp_simulator_pathsec_policies import BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping64AS
from bgp_simulator_pathsec_policies import BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping99AS
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
from bgp_simulator_pathsec_policies import GlobalEavesdropper
from bgp_simulator_pathsec_policies import GlobalEavesdropperUp
from bgp_simulator_pathsec_policies import TwoHopAttackUp
from bgp_simulator_pathsec_policies import OverheadAllSubgraph
from bgp_simulator_pathsec_policies import OverheadBPOAllSubgraph
from bgp_simulator_pathsec_policies import RibsInSizeSubgraph
from bgp_simulator_pathsec_policies import RibsInValidAdoptingSubgraph
from bgp_simulator_pathsec_policies import RibsInValidNonAdoptingSubgraph
from bgp_simulator_pathsec_policies import AdoptingCountSubgraph
from bgp_simulator_pathsec_policies import NonAdoptingCountSubgraph
from bgp_simulator_pathsec_policies import PathLengthSubgraph
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
from bgp_simulator_pathsec_policies import ValidSignature
from bgp_simulator_pathsec_policies import TransitiveDroppingAS
from bgp_simulator_pathsec_policies import TransitiveDropping2AS
from bgp_simulator_pathsec_policies import TransitiveDropping4AS
from bgp_simulator_pathsec_policies import TransitiveDropping8AS
from bgp_simulator_pathsec_policies import TransitiveDropping16AS
from bgp_simulator_pathsec_policies import TransitiveDropping32AS
from bgp_simulator_pathsec_policies import TransitiveDropping64AS
from bgp_simulator_pathsec_policies import TransitiveDropping99AS
from bgp_simulator_pathsec_policies import TransitiveDroppingAlwaysAS
from bgp_simulator_pathsec_policies import BGPsecTransitiveDownOnlyGlobalEavesdropperAS
from bgp_simulator_pathsec_policies import BGPsecTransitiveDownOnlyEncrUpGlobalEavesdropperAS


random.seed(os.environ['JOB_COMPLETION_INDEX'])
sim = Simulation(
    num_trials=7,
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
            # This says TimidLeak, it's really NoHashUpTimidLeak
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
        ValidSignature(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=OverheadBGPsecAS,
            BaseASCls=BGPAS),
        ValidSignature(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=OverheadBGPsecTransitiveDownOnlyAS,
            BaseASCls=BGPAS),
        GlobalEavesdropper(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=BGPsecTransitiveDownOnlyGlobalEavesdropperAS,
            BaseASCls=BGPAS),
        GlobalEavesdropperUp(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=BGPsecTransitiveDownOnlyEncrUpGlobalEavesdropperAS,
            BaseASCls=BGPAS),
        ShortestPathExportAllNoHashUp(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping1AS,
            BaseASCls=TransitiveDroppingAS),
        ShortestPathExportAllNoHashUp(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping2AS,
            BaseASCls=TransitiveDropping2AS),
        ShortestPathExportAllNoHashUp(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping4AS,
            BaseASCls=TransitiveDropping4AS),
        #ShortestPathExportAllNoHashUp(
        #    AnnCls=PathManipulationAnn, 
        #    AdoptASCls=BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping8AS,
        #    BaseASCls=TransitiveDropping8AS),
        #ShortestPathExportAllNoHashUp(
        #    AnnCls=PathManipulationAnn, 
        #    AdoptASCls=BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping16AS,
        #    BaseASCls=TransitiveDropping16AS),
        #ShortestPathExportAllNoHashUp(
        #    AnnCls=PathManipulationAnn, 
        #    AdoptASCls=BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping32AS,
        #    BaseASCls=TransitiveDropping32AS),
        #ShortestPathExportAllNoHashUp(
        #    AnnCls=PathManipulationAnn, 
        #    AdoptASCls=BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping64AS,
        #    BaseASCls=TransitiveDropping64AS),
        #ShortestPathExportAllNoHashUp(
        #    AnnCls=PathManipulationAnn, 
        #    AdoptASCls=BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping99AS,
        #    BaseASCls=TransitiveDropping99AS),
        ],
    propagation_rounds=2,
    subgraphs=[
        OverheadBPOAllSubgraph(),
        OverheadAllSubgraph(),
        AdoptingCountSubgraph(),
        NonAdoptingCountSubgraph(),
        AttackerSuccessAllSubgraph(),
        VictimSuccessAllSubgraph(),
        DisconnectedAllSubgraph(),
        PathLengthSubgraph(),
        RibsInSizeSubgraph(),
        RibsInValidAdoptingSubgraph(),
        RibsInValidNonAdoptingSubgraph(),
        AttackerSuccessAdoptingEtcSubgraph(),
        AttackerSuccessAdoptingInputCliqueSubgraph(),
        AttackerSuccessAdoptingStubsAndMHSubgraph(),
        AttackerSuccessNonAdoptingEtcSubgraph(),
        AttackerSuccessNonAdoptingInputCliqueSubgraph(),
        AttackerSuccessNonAdoptingStubsAndMHSubgraph(),
        DisconnectedAdoptingEtcSubgraph(),
        DisconnectedAdoptingInputCliqueSubgraph(),
        DisconnectedAdoptingStubsAndMHSubgraph(),
        DisconnectedNonAdoptingEtcSubgraph(),
        DisconnectedNonAdoptingInputCliqueSubgraph(),
        DisconnectedNonAdoptingStubsAndMHSubgraph(),
        VictimSuccessAdoptingEtcSubgraph(),
        VictimSuccessAdoptingInputCliqueSubgraph(),
        VictimSuccessAdoptingStubsAndMHSubgraph(),
        VictimSuccessNonAdoptingEtcSubgraph(),
        VictimSuccessNonAdoptingInputCliqueSubgraph(),
        VictimSuccessNonAdoptingStubsAndMHSubgraph(),
    ],
    percent_adoptions=[0.01, 0.1, 0.2, 0.3, 0.5, 0.8, 0.99],
    output_path=Path(f"ezgraphs{ os.environ['JOB_COMPLETION_INDEX'] }"),
    #output_path=Path(f"/tmp/ezgraphs{ os.environ['JOB_COMPLETION_INDEX'] }"),
    parse_cpus=1)

sim.run()

