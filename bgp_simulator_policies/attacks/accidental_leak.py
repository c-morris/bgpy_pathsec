from lib_bgp_simulator import BGPPolicy, Attack, Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario

from .. import DOAnn

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


