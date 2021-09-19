from lib_bgp_simulator import BGPPolicy, Attack, Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario, Graph

from .. import DOAnn

class AccidentalLeak(Attack):
    def __init__(self, attacker=ASNs.ATTACKER.value, victim=ASNs.VICTIM.value):
        anns = [DOAnn(prefix=Prefixes.PREFIX.value,
                    timestamp=Timestamps.VICTIM.value,
                    as_path=(victim,),
                    seed_asn=victim)]
        super(AccidentalLeak, self).__init__(attacker, victim, anns)
        
        self.round = 0
        self.post_run_hooks = [self.hook]

    def hook(self, s: Scenario):
        # Add the route leak from the attacker
        attacker_ann = None
        self.round += 1
        attacker_ann = s.engine.as_dict[self.attacker_asn].policy.local_rib.get(Prefixes.PREFIX.value)
        if self.round == 1:
            # If the attacker never received, the announcement, this attack is impossible, return
            if attacker_ann is None: 
                print("Attacker did not receive announcement from victim, cannot attack")
                print("Attacker RIB WAS", s.engine.as_dict[self.attacker_asn].policy.local_rib)
                return
            print("Altering the recv_relationship to customer for:", attacker_ann)
            s.engine.as_dict[self.attacker_asn].policy.local_rib[Prefixes.PREFIX.value].recv_relationship = Relationships.CUSTOMERS
