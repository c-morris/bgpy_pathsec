from bgpy import Prefixes, Relationships

from .intentional_leak import IntentionalLeak


class IntentionalLeakTimid(IntentionalLeak):
    """Same as IntentionalLeak, but timid.

    It will only leak if it can leak an announcement with no DO communities.
    """

    def post_propagation_hook(self, engine,
                              propagation_round, *args, **kwargs):
        """Add the route leak from the attacker"""
        attacker_ann = None
        attacker_asn = list(self.attacker_asns)[0]
        # Freeze this current ann in the local rib of the attacker
        attacker_ann = engine.as_dict[attacker_asn]._local_rib.get_ann(Prefixes.PREFIX.value) # noqa E501
        if attacker_ann is not None:
            attacker_ann.seed_asn = attacker_asn
        attacker = engine.as_dict[attacker_asn]
        if propagation_round == 0:
            attack_anns = []
            for ann_info in attacker._ribs_in.get_ann_infos(Prefixes.PREFIX.value): # noqa E501
                atk_ann = attacker._copy_and_process(ann_info.unprocessed_ann, Relationships.CUSTOMERS) # noqa E501
                # Truncate path as much as possible, which is to the AS
                # after the most recent BGPsec Transitive adopter on the
                # path
                prev_len = len(atk_ann.as_path)
                self._truncate_ann(atk_ann)

                # Clear any down only communities
                self._trim_do_communities(atk_ann)
                if len(atk_ann.do_communities) > 0:
                    # If there are any DO communities, this is un-leakable
                    continue

                # Reprocess atk_ann to add the attacker's ASN
                if prev_len != len(atk_ann.as_path):
                    atk_ann = attacker._copy_and_process(atk_ann, Relationships.CUSTOMERS) # noqa E501
                attack_anns.append(atk_ann)

            def pathlen(ann):
                return len(ann.as_path)
            attack_anns = sorted(attack_anns, key=pathlen)

            if len(attack_anns) == 0:
                print("Attacker did not receive announcement from victim, cannot attack") # noqa E501
                return

            self.leak_announcements_to_providers(
                attack_anns, attacker, propagation_round)
