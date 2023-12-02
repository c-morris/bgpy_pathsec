import os
import random
from pathlib import Path

from bgpy import Simulation, BGPAS
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
from bgpy_pathsec import Eavesdropper
from bgpy_pathsec import OverheadAllSubgraph
from bgpy_pathsec import OverheadBPOAllSubgraph
from bgpy_pathsec import RibsInSizeSubgraph
from bgpy_pathsec import RibsInValidAdoptingSubgraph
from bgpy_pathsec import RibsInValidNonAdoptingSubgraph
from bgpy_pathsec import AdoptingCountSubgraph
from bgpy_pathsec import NonAdoptingCountSubgraph
from bgpy_pathsec import PathLengthSubgraph
from bgpy_pathsec import BGPsecTransitiveDownOnlyEncrUpGlobalEavesdropperAS
from bgpy_pathsec import KAPKFalseAS
from bgpy_pathsec import KAPKFalse01AS
from bgpy_pathsec import KAPKFalse05AS
from bgpy_pathsec import KAPKFalse5AS



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

