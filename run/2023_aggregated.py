import os
import random
from multiprocessing import cpu_count
from pathlib import Path

from bgpy import BGPAS
from bgpy.subgraph_simulation_framework import AttackerSuccessAllSubgraph
from bgpy.subgraph_simulation_framework import DisconnectedAllSubgraph
from bgpy.subgraph_simulation_framework import VictimSuccessAllSubgraph

from bgpy.subgraph_simulation_framework import (
    AttackerSuccessAdoptingEtcSubgraph,
)
from bgpy.subgraph_simulation_framework import (
    AttackerSuccessAdoptingInputCliqueSubgraph,
)
from bgpy.subgraph_simulation_framework import (
    AttackerSuccessAdoptingStubsAndMHSubgraph,
)
from bgpy.subgraph_simulation_framework import (
    AttackerSuccessNonAdoptingEtcSubgraph,
)
from bgpy.subgraph_simulation_framework import (
    AttackerSuccessNonAdoptingInputCliqueSubgraph,
)
from bgpy.subgraph_simulation_framework import (
    AttackerSuccessNonAdoptingStubsAndMHSubgraph,
)

from bgpy.subgraph_simulation_framework import DisconnectedAdoptingEtcSubgraph
from bgpy.subgraph_simulation_framework import (
    DisconnectedAdoptingInputCliqueSubgraph,
)
from bgpy.subgraph_simulation_framework import (
    DisconnectedAdoptingStubsAndMHSubgraph,
)
from bgpy.subgraph_simulation_framework import (
    DisconnectedNonAdoptingEtcSubgraph,
)
from bgpy.subgraph_simulation_framework import (
    DisconnectedNonAdoptingInputCliqueSubgraph,
)
from bgpy.subgraph_simulation_framework import (
    DisconnectedNonAdoptingStubsAndMHSubgraph,
)

from bgpy.subgraph_simulation_framework import VictimSuccessAdoptingEtcSubgraph
from bgpy.subgraph_simulation_framework import (
    VictimSuccessAdoptingInputCliqueSubgraph,
)
from bgpy.subgraph_simulation_framework import (
    VictimSuccessAdoptingStubsAndMHSubgraph,
)
from bgpy.subgraph_simulation_framework import (
    VictimSuccessNonAdoptingEtcSubgraph,
)
from bgpy.subgraph_simulation_framework import (
    VictimSuccessNonAdoptingInputCliqueSubgraph,
)
from bgpy.subgraph_simulation_framework import (
    VictimSuccessNonAdoptingStubsAndMHSubgraph,
)

from bgpy_pathsec import PathManipulationAnn
from bgpy_pathsec import BGPsecAggressiveAS
from bgpy_pathsec import BGPsecTransitiveAggressiveAS
from bgpy_pathsec import BGPsecTransitiveDownOnlyAggressiveAS
from bgpy_pathsec import BGPsecTransitiveTimidAS
from bgpy_pathsec import BGPsecTransitiveDownOnlyTimidAS
from bgpy_pathsec import BGPsecTransitiveDownOnlyNoHashTimidAS
from bgpy_pathsec import (
    BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping1AS,
)
from bgpy_pathsec import (
    BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping2AS,
)
from bgpy_pathsec import (
    BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping4AS,
)
from bgpy_pathsec import OriginHijack
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
from bgpy_pathsec import BGPsecTransitiveDownOnlyGlobalEavesdropperAS
from bgpy_pathsec import BGPsecTransitiveDownOnlyEncrUpGlobalEavesdropperAS

# New
from bgpy_pathsec import PathsecScenarioConfig
from bgpy.subgraph_simulation_framework import SubgraphSimulation


random.seed(os.environ.get("JOB_COMPLETION_INDEX", 0))
sim = SubgraphSimulation(
    num_trials=1,
    scenario_configs=[
        PathsecScenarioConfig(
            ScenarioCls=OriginHijack,
            AnnCls=PathManipulationAnn,
            AdoptASCls=BGPsecAggressiveAS,
            BaseASCls=BGPAS,
        ),
        # BGPsec Timid never makes sense, aggressive is always better
        # ShortestPathExportAll(
        #     AnnCls=PathManipulationAnn,
        #     AdoptASCls=BGPsecTimidAS,
        #     BaseASCls=BGPAS),
        PathsecScenarioConfig(
            ScenarioCls=OriginHijack,
            AnnCls=PathManipulationAnn,
            AdoptASCls=BGPsecTransitiveAggressiveAS,
            BaseASCls=BGPAS,
        ),
        PathsecScenarioConfig(
            ScenarioCls=ShortestPathExportAll,
            AnnCls=PathManipulationAnn,
            # All BGPsecTransitive attacks must be NoHash
            AdoptASCls=BGPsecTransitiveTimidAS,
            BaseASCls=BGPAS,
            communities_up=False,
        ),
        PathsecScenarioConfig(
            ScenarioCls=OriginHijack,
            AnnCls=PathManipulationAnn,
            AdoptASCls=BGPsecTransitiveDownOnlyAggressiveAS,
            BaseASCls=BGPAS,
        ),
        PathsecScenarioConfig(
            ScenarioCls=ShortestPathExportAll,
            AnnCls=PathManipulationAnn,
            AdoptASCls=BGPsecTransitiveDownOnlyTimidAS,
            BaseASCls=BGPAS,
        ),
        PathsecScenarioConfig(
            ScenarioCls=ShortestPathExportAll,
            AnnCls=PathManipulationAnn,
            AdoptASCls=BGPsecTransitiveDownOnlyUpTimidAS,
            BaseASCls=BGPAS,
            no_hash=False,
        ),
        PathsecScenarioConfig(
            ScenarioCls=ShortestPathExportAll,
            AnnCls=PathManipulationAnn,
            AdoptASCls=BGPsecTransitiveDownOnlyNoHashTimidAS,
            BaseASCls=BGPAS,
            communities_up=False,
        ),
        PathsecScenarioConfig(
            ScenarioCls=ShortestPathExportAll,
            AnnCls=PathManipulationAnn,
            AdoptASCls=BGPsecTransitiveDownOnlyNoHashUpTimidAS,
            BaseASCls=BGPAS,
        ),
        PathsecScenarioConfig(
            ScenarioCls=OriginHijack,
            AnnCls=PathManipulationAnn,
            AdoptASCls=PathEndAggressiveAS,
            BaseASCls=BGPAS,
        ),
        PathsecScenarioConfig(
            ScenarioCls=TwoHopAttack,
            AnnCls=PathManipulationAnn,
            AdoptASCls=PathEndTimidAS,
            BaseASCls=BGPAS,
            communities_up=False,
        ),
        PathsecScenarioConfig(
            ScenarioCls=TwoHopAttack,
            AnnCls=PathManipulationAnn,
            AdoptASCls=PathEndTimidUpAS,
            BaseASCls=BGPAS,
        ),
        PathsecScenarioConfig(
            ScenarioCls=OriginHijack,
            AnnCls=PathManipulationAnn,
            AdoptASCls=BaselineBGPAS,
            BaseASCls=BGPAS,
        ),
        PathsecScenarioConfig(
            ScenarioCls=Eavesdropper,
            AnnCls=PathManipulationAnn,
            AdoptASCls=BGPsecTransitiveDownOnlyGlobalEavesdropperAS,
            BaseASCls=BGPAS,
            no_hash=False,
            communities_up=False,
        ),
        PathsecScenarioConfig(
            ScenarioCls=Eavesdropper,
            AnnCls=PathManipulationAnn,
            AdoptASCls=BGPsecTransitiveDownOnlyEncrUpGlobalEavesdropperAS,
            BaseASCls=BGPAS,
            no_hash=False,
        ),
        PathsecScenarioConfig(
            ScenarioCls=ShortestPathExportAll,
            AnnCls=PathManipulationAnn,
            AdoptASCls=BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping1AS,
            BaseASCls=TransitiveDroppingAS,
        ),
        PathsecScenarioConfig(
            ScenarioCls=ShortestPathExportAll,
            AnnCls=PathManipulationAnn,
            AdoptASCls=BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping2AS,
            BaseASCls=TransitiveDropping2AS,
        ),
        PathsecScenarioConfig(
            ScenarioCls=ShortestPathExportAll,
            AnnCls=PathManipulationAnn,
            AdoptASCls=BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping4AS,
            BaseASCls=TransitiveDropping4AS,
        ),
        # Must be at the end since this has 0 attackers
        PathsecScenarioConfig(
            ScenarioCls=ValidSignature,
            AnnCls=PathManipulationAnn,
            AdoptASCls=OverheadBGPsecAS,
            BaseASCls=BGPAS,
        ),
        PathsecScenarioConfig(
            ScenarioCls=ValidSignature,
            AnnCls=PathManipulationAnn,
            AdoptASCls=OverheadBGPsecTransitiveDownOnlyAS,
            BaseASCls=BGPAS,
        ),
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
    percent_adoptions=[.5],#[0.01, 0.1, 0.2, 0.3, 0.5, 0.8, 0.99],
    output_path=Path(f"ezgraphs{ os.environ.get('JOB_COMPLETION_INDEX', 0)}"),
    # output_path=Path(f"/tmp/ezgraphs{ os.environ['JOB_COMPLETION_INDEX'] }"),
    parse_cpus=1,#cpu_count(),
)
print("about to run sims")
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()
sim.run(include_graphs=False)
profiler.disable()
# Write the stats to a file, sorted by 'cumulative' time
with open('/tmp/profile_stats.txt', 'w') as file:
    stats = pstats.Stats(profiler, stream=file)
    stats.sort_stats('cumulative')
    stats.print_stats()
