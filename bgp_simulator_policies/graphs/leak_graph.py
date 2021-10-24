from lib_bgp_simulator import Graph


class LeakGraph(Graph):
    def _get_subgraphs(self, engine=None):
        """Add a multihome subgraph"""

        subgraphs = super(LeakGraph, self)._get_subgraphs(engine)

        subgraphs["mh"] = set([x.asn for x in engine if x.multihomed])
        subgraphs["stubs"] = set([x.asn for x in engine if x.stub])

        del subgraphs["stubs_and_mh"]

        return subgraphs
