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
from bgp_simulator_pathsec_policies import TransitiveDroppingConversionsAllSubgraph
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
from bgp_simulator_pathsec_policies import TransitiveDroppingNoAdoptCustomersAS
from bgp_simulator_pathsec_policies import BGPsecTransitiveDownOnlyGlobalEavesdropperAS
from bgp_simulator_pathsec_policies import BGPsecTransitiveDownOnlyEncrUpGlobalEavesdropperAS
from bgp_simulator_pathsec_policies import BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers1AS
from bgp_simulator_pathsec_policies import BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers2AS
from bgp_simulator_pathsec_policies import BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers4AS
from bgp_simulator_pathsec_policies import TransitiveDroppingNoAdoptCustomersAS
from bgp_simulator_pathsec_policies import TransitiveDroppingNoAdoptCustomers2AS
from bgp_simulator_pathsec_policies import TransitiveDroppingNoAdoptCustomers4AS

random.seed(os.environ['JOB_COMPLETION_INDEX'])
sim = Simulation(
    num_trials=70,
    scenarios=[
        ShortestPathExportAllNoHashUp(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers1AS,
            BaseASCls=TransitiveDroppingNoAdoptCustomersAS),
        ShortestPathExportAllNoHashUp(
            AnnCls=PathManipulationAnn, 
            AdoptASCls=BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers2AS,
            BaseASCls=TransitiveDroppingNoAdoptCustomers2AS),
        ShortestPathExportAllNoHashUp(
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
    output_path=Path(f"/data/ezgraphs{ os.environ['JOB_COMPLETION_INDEX'] }"),
    #output_path=Path(f"/tmp/ezgraphs{ os.environ['JOB_COMPLETION_INDEX'] }"),
    parse_cpus=1)

sim.run()
