import os
import random
from pathlib import Path

from bgpy import Simulation
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
from bgpy_pathsec import OverheadAllSubgraph
from bgpy_pathsec import OverheadBPOAllSubgraph
from bgpy_pathsec import RibsInSizeSubgraph
from bgpy_pathsec import RibsInValidAdoptingSubgraph
from bgpy_pathsec import RibsInValidNonAdoptingSubgraph
from bgpy_pathsec import AdoptingCountSubgraph
from bgpy_pathsec import NonAdoptingCountSubgraph
from bgpy_pathsec import PathLengthSubgraph
from bgpy_pathsec import TransitiveDroppingConversionsAllSubgraph
from bgpy_pathsec import ShortestPathExportAll
from bgpy_pathsec import TransitiveDroppingNoAdoptCustomersAS
from bgpy_pathsec import BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers1AS
from bgpy_pathsec import BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers2AS
from bgpy_pathsec import BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers4AS
from bgpy_pathsec import TransitiveDroppingNoAdoptCustomersAS
from bgpy_pathsec import TransitiveDroppingNoAdoptCustomers2AS
from bgpy_pathsec import TransitiveDroppingNoAdoptCustomers4AS

random.seed(os.environ['JOB_COMPLETION_INDEX'])
sim = Simulation(
    num_trials=7,
    scenarios=[
        ShortestPathExportAll(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers1AS,
            BaseASCls=TransitiveDroppingNoAdoptCustomersAS),
        ShortestPathExportAll(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers2AS,
            BaseASCls=TransitiveDroppingNoAdoptCustomers2AS),
        ShortestPathExportAll(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers4AS,
            BaseASCls=TransitiveDroppingNoAdoptCustomers4AS),
            ],
    propagation_rounds=3,
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
        TransitiveDroppingConversionsAllSubgraph(),
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
    output_path=Path(f"tdgraphs{ os.environ['JOB_COMPLETION_INDEX'] }"),
    #output_path=Path(f"/tmp/ezgraphs{ os.environ['JOB_COMPLETION_INDEX'] }"),
    parse_cpus=1)

sim.run()

