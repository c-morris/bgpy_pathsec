import os
import random
from datetime import date
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
from bgpy_pathsec import TransitiveDroppingNoAdoptCustomers
from bgpy_pathsec import BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers1AS
from bgpy_pathsec import BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers2AS
from bgpy_pathsec import BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers4AS
from bgpy_pathsec import BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers8AS
from bgpy_pathsec import BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers16AS
from bgpy_pathsec import TransitiveDroppingNoAdoptCustomers

# New
from bgpy_pathsec import PathsecScenarioConfig
from bgpy.subgraph_simulation_framework import SubgraphSimulation


random.seed(os.environ.get('JOB_COMPLETION_INDEX', 0))
sim = SubgraphSimulation(
    num_trials=7,
    scenario_configs=[
        PathsecScenarioConfig(
            ScenarioCls=TransitiveDroppingNoAdoptCustomers,
            AnnCls=PathManipulationAnn,
            AdoptASCls=BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers1AS,
            BaseASCls=BGPAS,
            transitive_dropping_percent=1,
        ),
        PathsecScenarioConfig(
            ScenarioCls=TransitiveDroppingNoAdoptCustomers,
            AnnCls=PathManipulationAnn,
            AdoptASCls=BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers2AS,
            BaseASCls=BGPAS,
            transitive_dropping_percent=2,
        ),
        PathsecScenarioConfig(
            ScenarioCls=TransitiveDroppingNoAdoptCustomers,
            AnnCls=PathManipulationAnn,
            AdoptASCls=BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers4AS,
            BaseASCls=BGPAS,
            transitive_dropping_percent=4
        ),
        PathsecScenarioConfig(
            ScenarioCls=TransitiveDroppingNoAdoptCustomers,
            AnnCls=PathManipulationAnn,
            AdoptASCls=BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers8AS,
            BaseASCls=BGPAS,
            transitive_dropping_percent=8
        ),
        PathsecScenarioConfig(
            ScenarioCls=TransitiveDroppingNoAdoptCustomers,
            AnnCls=PathManipulationAnn,
            AdoptASCls=BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers16AS,
            BaseASCls=BGPAS,
            transitive_dropping_percent=16
        ),

            ],
    propagation_rounds=1,
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
    output_path=Path(f"tdgraphs{ os.environ.get('JOB_COMPLETION_INDEX', 0) }"),
    #output_path=Path(f"/tmp/ezgraphs{ os.environ['JOB_COMPLETION_INDEX'] }"),
    caida_run_kwargs={
            "dl_time": date.fromisoformat('2022-09-01'),
            "cache_dir": Path("caida_collector_cache"),
            "tsv_path": Path("caida_collector.tsv")
    },
    parse_cpus=1)

sim.run(include_graphs=False)
