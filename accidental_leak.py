from lib_bgp_simulator import Simulator, Graph, ROVPolicy, SubprefixHijack, BGPPolicy
from lib_bgp_simulator import Attack, Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario

class DOAnn(Announcement):
    """Down-Only Community Announcement"""

    __slots__ = ["do_communities",]

    def __init__(self, *args, **kwargs):
        super(DOAnn, self).__init__(*args, **kwargs)
        # do_communities is a tuple of ASNs which are added to the announcement with the down-only community
        self.do_communities = tuple()

class AccidentalLeak(Attack):
    def __init__(self, attacker=ASNs.ATTACKER.value, victim=ASNs.VICTIM.value):
        anns = [DOAnn(prefix=Prefixes.PREFIX.value,
                    timestamp=Timestamps.VICTIM.value,
                    as_path=(victim,),
                    seed_asn=victim)]
        super(AccidentalLeak, self).__init__(attacker, victim, anns)
        self.round = 0
        def hook(s: Scenario):
            # Add the route leak from the attacker
            attacker_ann = None
            self.round += 1
            if self.round == 1:
                attacker_ann = s.engine.as_dict[attacker].policy.local_rib.get(Prefixes.PREFIX.value)
                # If the attacker never received, the announcement, this attack is impossible, return
                if attacker_ann is None: 
                    print("Attacker did not receive announcement from victim, cannot attack")
                    print("Attacker RIB WAS", s.engine.as_dict[attacker].policy.local_rib)
                    return
                print("Seeding attack announcement:", attacker_ann)
                atk_ann = DOAnn(prefix=Prefixes.PREFIX.value,
                    timestamp=Timestamps.ATTACKER.value,
                    as_path=attacker_ann.as_path,
                    seed_asn=attacker)
                atk_ann.recv_relationship = Relationships.CUSTOMERS
                self.announcements.append(atk_ann)
        self.post_run_hooks = [hook]

graphs = [Graph(percent_adoptions=[0, 5],
                adopt_policies=[BGPPolicy], # change to DO policy
                AttackCls=AccidentalLeak,
                num_trials=1,
                propagation_rounds=2,
                base_policy=BGPPolicy)]
Simulator().run(graphs=graphs)

# Dealing with output data (not in the code yet)
for graph in graphs:
    for data_point, list_of_scenarios in graph.data_points.items():
        print("Percent adoption", data_point.percent_adoption)
        print("Adopted policy:", data_point.PolicyCls.name)
        print("Propagation round", data_point.propagation_round)
        for scenario in list_of_scenarios:
            print(scenario.data)


