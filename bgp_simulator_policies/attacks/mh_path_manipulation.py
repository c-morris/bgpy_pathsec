from lib_bgp_simulator import EngineInput

from .. import PathManipulationAnn


class MHPathManipulation(EngineInput):

    AnnCls = PathManipulationAnn

    def _possible_attackers(self, subgraph_asns, engine):
        return subgraph_asns["mh"]

    def _possible_victims(self, subgraph_asns, engine):
        return subgraph_asns["mh"]
