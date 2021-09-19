from lib_bgp_simulator import BGPPolicy, Attack, Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario

from .. import PAnn

class OriginHijack(Attack):
    """Origin hijack with a *fake* path"""
    def __init__(self, attacker=ASNs.ATTACKER.value, victim=ASNs.VICTIM.value):
        anns = [PAnn(prefix=Prefixes.PREFIX.value,
                    timestamp=Timestamps.VICTIM.value,
                    as_path=(victim,),
                    seed_asn=victim),
                PAnn(prefix=Prefixes.PREFIX.value,
                    timestamp=Timestamps.ATTACKER.value,
                    # 64555 is a private ASN, it should not exist in the AS graph
                    as_path=(attacker, 64555, victim),
                    seed_asn=attacker),]
        super(OriginHijack, self).__init__(attacker, victim, anns)

        self.post_run_hooks = []
