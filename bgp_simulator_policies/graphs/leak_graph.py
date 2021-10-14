import random

from lib_bgp_simulator import Attack, Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario, Graph

from .custom_graph import CustomGraph

class LeakGraph(CustomGraph):
    def _get_subgraphs(self, engine):
        """Add a multihome subgraph"""

        subgraphs = Graph._get_subgraphs(self, engine)
        stubs = set([x.asn for x in engine.as_dict.values()
                            if x.stub])
        mh = set([x.asn for x in engine.as_dict.values()
                            if x.multihomed])
        del subgraphs["stubs_and_mh"]
        subgraphs["mh"] = mh
        subgraphs["stubs"] = stubs
        return subgraphs

    def _get_attack(self):
        return self.AttackCls(*random.sample(self.subgraphs["mh"], 2))
