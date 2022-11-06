from caida_collector_pkg import CaidaCollector
from bgp_simulator_pkg import BGPSimpleAS, SimulationEngine


class ProviderConeComputation:
    """Compute provider cones for every AS in the CAIDA topology."""

    def __init__(self):
        self.engine = CaidaCollector(BaseASCls=BGPSimpleAS,
                                GraphCls=SimulationEngine,
                                ).run(tsv_path=None)
        # Initialize
        self.provider_cones = dict()
        for as_obj in self.engine.ases:
            self.provider_cones[as_obj.asn] = set()

    def get_cone(self, as_obj):
        """Compute a provider cone for a single AS"""
        if as_obj.input_clique or len(self.provider_cones[as_obj.asn]) > 0:
            return
        asns_in_cone = set()
        for provider_obj in as_obj.providers:
            if len(self.provider_cones[provider_obj.asn]) == 0:
                self.get_cone(provider_obj)
            asns_in_cone.union(self.provider_cones[provider_obj.asn])
            asns_in_cone.add(provider_obj.asn)
        self.provider_cones[as_obj.asn] = asns_in_cone

    def get_all_cones(self):
        """Populate self.provider_cones for every AS"""
        for as_obj in self.engine.ases:
            self.get_cone(as_obj)


if __name__ == "__main__":
    a = ProviderConeComputation()
    a.get_all_cones()
    h_max = 11
    histogram = [0 for i in range(h_max)]
    for asn, cone in a.provider_cones.items():
        if len(cone) < h_max:
            histogram[len(cone)] += 1
    print("Number of provider cones of size x")
    for i in range(h_max):
        print(f"{i}\t{histogram[i]}")
