from lib_bgp_simulator import Attack, Prefixes, Timestamps, ASNs, Announcement, Relationships, Scenario, Graph, SimulatorEngine, DataPoint

from .. import PAnn

class OriginHijack(Attack):
    """Origin hijack with a *fake* path"""
    def __init__(self, attacker=ASNs.ATTACKER.value, victim=ASNs.VICTIM.value):
        anns = [PAnn(prefix=Prefixes.PREFIX.value,
                    timestamp=Timestamps.VICTIM.value,
                    as_path=(victim,),
                    # Legitimate announcement has valid BGPsec attributes
                    bgpsec_path=(victim,),
                    next_as=victim,
                    seed_asn=victim,
                    recv_relationship=Relationships.ORIGIN),
                PAnn(prefix=Prefixes.PREFIX.value,
                    timestamp=Timestamps.ATTACKER.value,
                    as_path=(attacker, victim),
                    seed_asn=attacker,
                    # Add victim to removed signatures
                    removed_signatures=(victim,),
                    recv_relationship=Relationships.ORIGIN),]
        super(OriginHijack, self).__init__(attacker, victim, anns)

        self.post_run_hooks = []
