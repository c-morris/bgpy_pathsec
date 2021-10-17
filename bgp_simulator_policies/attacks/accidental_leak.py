from lib_bgp_simulator import BGPAS, Attack, Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario, Graph, SimulatorEngine, DataPoint, ROAValidity

from .. import PAnn

class AccidentalLeak(Attack):
    def __init__(self, attacker=ASNs.ATTACKER.value, victim=ASNs.VICTIM.value):
        anns = [PAnn(prefix=Prefixes.PREFIX.value,
                    timestamp=Timestamps.VICTIM.value,
                    as_path=(victim,),
                    bgpsec_path=(victim,),
                    removed_signatures = tuple(),
                    next_as=victim,
                    do_communities = tuple(),
                    roa_validity = ROAValidity.UNKNOWN,
                    withdraw = False,
                    traceback_end = True,
                    seed_asn=victim,
                    recv_relationship=Relationships.ORIGIN)]

        super(AccidentalLeak, self).__init__(attacker, victim, anns)
        
        self.post_run_hooks = [self.hook]

    def hook(self, engine: SimulatorEngine, prev_data_point: DataPoint):
        # Add the route leak from the attacker
        attacker_ann = None
        attacker_ann = engine.as_dict[self.attacker_asn].local_rib.get_ann(Prefixes.PREFIX.value)
        if prev_data_point.propagation_round == 0:
            # If the attacker never received, the announcement, this attack is impossible, return
            if attacker_ann is None: 
                print("Attacker did not receive announcement from victim, cannot attack")
                print("Attacker RIB WAS", engine.as_dict[self.attacker_asn].local_rib)
                return
            print("Altering the recv_relationship to customer for:", attacker_ann)
            engine.as_dict[self.attacker_asn].local_rib.get_ann(Prefixes.PREFIX.value).recv_relationship = Relationships.CUSTOMERS
