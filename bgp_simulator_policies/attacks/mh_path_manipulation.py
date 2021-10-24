from lib_bgp_simulator import EngineInput

from .. import PAnn

class MHPathManipulation(EngineInput):

    AnnCls = PAnn
    def _possible_attackers(self, subgraph_asns, engine):
        return subgraph_asns["mh"]

    def _possible_victims(self, subgraph_asns, engine):
        return subgraph_asns["mh"]
