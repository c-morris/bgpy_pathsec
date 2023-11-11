from bgpy import Prefixes, Relationships, Timestamps, ValidPrefix


class ValidSignature(ValidPrefix):
    """ValidPrefix, but with valid BGPsec Signatures.

    This is for comparing overhead (without attacks) between BGPsec and BGPsec
    Transitive variants.
    """

    def _get_announcements(self, *args, **kwargs):
        """Returns a valid prefix announcement, with bgpsec signatures."""

        anns = list()
        for victim_asn in self.victim_asns:
            anns.append(
                self.scenario_config.AnnCls(
                    prefix=Prefixes.PREFIX.value,
                    as_path=(victim_asn,),
                    timestamp=Timestamps.VICTIM.value,
                    seed_asn=victim_asn,
                    roa_valid_length=True,
                    roa_origin=victim_asn,
                    recv_relationship=Relationships.ORIGIN,
                    next_as=victim_asn,
                    do_communities=tuple(),
                    bgpsec_path=(victim_asn,),
                    removed_signatures=tuple(),
                    withdraw=False,
                    traceback_end=True,
                    communities=tuple(),
                )
            )
        return tuple(anns)
