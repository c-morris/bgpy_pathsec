import os
import random
from pathlib import Path

from bgpy import Simulation, BGPAS
from bgpy import Prefixes
from bgpy import Timestamps
from bgpy import ASNs
from bgpy import Announcement
from bgpy import Relationships
from bgpy import Scenario
from bgpy import AttackerSuccessAllSubgraph
from bgpy import DisconnectedAllSubgraph
from bgpy import VictimSuccessAllSubgraph

from bgpy import AttackerSuccessAdoptingEtcSubgraph
from bgpy import AttackerSuccessAdoptingInputCliqueSubgraph
from bgpy import AttackerSuccessAdoptingStubsAndMHSubgraph
from bgpy import AttackerSuccessNonAdoptingEtcSubgraph
from bgpy import AttackerSuccessNonAdoptingInputCliqueSubgraph
from bgpy import AttackerSuccessNonAdoptingStubsAndMHSubgraph

from bgpy import DisconnectedAdoptingEtcSubgraph
from bgpy import DisconnectedAdoptingInputCliqueSubgraph
from bgpy import DisconnectedAdoptingStubsAndMHSubgraph
from bgpy import DisconnectedNonAdoptingEtcSubgraph
from bgpy import DisconnectedNonAdoptingInputCliqueSubgraph
from bgpy import DisconnectedNonAdoptingStubsAndMHSubgraph

from bgpy import VictimSuccessAdoptingEtcSubgraph
from bgpy import VictimSuccessAdoptingInputCliqueSubgraph
from bgpy import VictimSuccessAdoptingStubsAndMHSubgraph
from bgpy import VictimSuccessNonAdoptingEtcSubgraph
from bgpy import VictimSuccessNonAdoptingInputCliqueSubgraph
from bgpy import VictimSuccessNonAdoptingStubsAndMHSubgraph

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

from bgpy.bgpy import Simulation
from bgpy.bgpy import ScenarioConfig

# TODO: Finish updating simulation
sim = Simulation(
    percent_adoptions=(0.01, 0.1, 0.2, 0.3, 0.5, 0.8, 0.99),
    num_trials=1,
    scenario_configs=(
        ScenarioConfig(ScenarioCls=OriginHijack, AdoptASCls=BGPsecAggressiveAS, BaseASCls=BGPAS)
    ),

    propagation_rounds=2,
    output_dir=Path(f"/data/ezgraphs{ os.environ['JOB_COMPLETION_INDEX'] }"),
    #output_path=Path(f"/tmp/ezgraphs{ os.environ['JOB_COMPLETION_INDEX'] }"),
    parse_cpus=1
)


random.seed(os.environ['JOB_COMPLETION_INDEX'])
sim = Simulation(
    num_trials=1,
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
    output_path=Path(f"/data/ezgraphs{ os.environ['JOB_COMPLETION_INDEX'] }"),
    #output_path=Path(f"/tmp/ezgraphs{ os.environ['JOB_COMPLETION_INDEX'] }"),
    parse_cpus=1)

sim.run()
