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

from bgpy_pathsec import PathManipulationAnn
from bgpy_pathsec import PathEndAS
from bgpy_pathsec import BGPsecAggressiveAS
from bgpy_pathsec import BGPsecTransitiveAggressiveAS
from bgpy_pathsec import BGPsecTransitiveDownOnlyAggressiveAS
from bgpy_pathsec import BGPsecTransitiveTimidAS
from bgpy_pathsec import BGPsecTransitiveDownOnlyTimidAS
from bgpy_pathsec import BGPsecTransitiveDownOnlyNoHashTimidAS
from bgpy_pathsec import BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping1AS
from bgpy_pathsec import BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping2AS
from bgpy_pathsec import BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping4AS
from bgpy_pathsec import BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping8AS
from bgpy_pathsec import BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping16AS
from bgpy_pathsec import BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping32AS
from bgpy_pathsec import BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping64AS
from bgpy_pathsec import BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping99AS
from bgpy_pathsec import BGPsecTransitiveDownOnlyNoHashAggressiveAS
from bgpy_pathsec import BGPsecTimidAS
from bgpy_pathsec import BGPsecTransitiveDownOnlyTimidLeakAS
from bgpy_pathsec import OriginHijack
from bgpy_pathsec import IntentionalLeak
from bgpy_pathsec import BGPsecAS
from bgpy_pathsec import BGPsecTransitiveAS
from bgpy_pathsec import BGPsecTransitiveDownOnlyAS
from bgpy_pathsec import TwoHopAttack
from bgpy_pathsec import Eavesdropper
from bgpy_pathsec import OverheadAllSubgraph
from bgpy_pathsec import OverheadBPOAllSubgraph
from bgpy_pathsec import RibsInSizeSubgraph
from bgpy_pathsec import RibsInValidAdoptingSubgraph
from bgpy_pathsec import RibsInValidNonAdoptingSubgraph
from bgpy_pathsec import AdoptingCountSubgraph
from bgpy_pathsec import NonAdoptingCountSubgraph
from bgpy_pathsec import PathLengthSubgraph
from bgpy_pathsec import ShortestPathExportAll
from bgpy_pathsec import BGPsecTransitiveDownOnlyNoHashUpTimidAS
from bgpy_pathsec import PathEndAggressiveAS
from bgpy_pathsec import PathEndTimidAS
from bgpy_pathsec import BaselineBGPAS
from bgpy_pathsec import PathEndTimidUpAS
from bgpy_pathsec import BGPsecTransitiveDownOnlyUpTimidAS
from bgpy_pathsec import OverheadBGPsecAS
from bgpy_pathsec import OverheadBGPsecTransitiveDownOnlyAS
from bgpy_pathsec import ValidSignature
from bgpy_pathsec import TransitiveDroppingAS
from bgpy_pathsec import TransitiveDropping2AS
from bgpy_pathsec import TransitiveDropping4AS
from bgpy_pathsec import TransitiveDropping8AS
from bgpy_pathsec import TransitiveDropping16AS
from bgpy_pathsec import TransitiveDropping32AS
from bgpy_pathsec import TransitiveDropping64AS
from bgpy_pathsec import TransitiveDropping99AS
from bgpy_pathsec import TransitiveDroppingAlwaysAS
from bgpy_pathsec import BGPsecTransitiveDownOnlyGlobalEavesdropperAS
from bgpy_pathsec import BGPsecTransitiveDownOnlyEncrUpGlobalEavesdropperAS
from bgpy_pathsec import BGPsecTransitiveDownOnlyEncrUpGlobalEavesdropperUnknownAdoptersAS
from bgpy_pathsec import KAPKFalseAS
from bgpy_pathsec import KAPKFalse01AS
from bgpy_pathsec import KAPKFalse05AS
from bgpy_pathsec import KAPKFalse5AS
from bgpy_pathsec import KAPKFalseAlwaysAS
from bgpy_pathsec import KAPKFalseNeverAS



random.seed(os.environ['JOB_COMPLETION_INDEX'])
sim = Simulation(
    num_trials=7,
    scenarios=[
        #ShortestPathExportAllUpUnknownAdopters(
        #   AnnCls=PathManipulationAnn, 
        #   AdoptASCls=KAPKFalseAS,  
        #   BaseASCls=BGPsecTransitiveAS),
        Eavesdropper(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=KAPKFalse01AS,
            BaseASCls=BGPAS,
            unknown_adopter=True),
        Eavesdropper(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=KAPKFalse05AS,
            BaseASCls=BGPAS,
            unknown_adopter=True),
        Eavesdropper(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=KAPKFalseAS,
            BaseASCls=BGPAS,
            unknown_adopter=True),
        Eavesdropper(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=KAPKFalse5AS,
            BaseASCls=BGPAS,
            unknown_adopter=True),
        Eavesdropper(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=BGPsecTransitiveDownOnlyEncrUpGlobalEavesdropperAS,
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
    output_path=Path(f"kapkgraphs{ os.environ['JOB_COMPLETION_INDEX'] }"),
    #output_path=Path("/tmp/kapkgraphs0"),
    parse_cpus=1)

sim.run()

