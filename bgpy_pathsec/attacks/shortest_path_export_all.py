from .intentional_leak import IntentionalLeak


class ShortestPathExportAll(IntentionalLeak):
    """Shortest path Export all strategy, from other works.
    Only leaks a single path (the shortest one) to providers.
    """

    def leak_announcements_to_providers(
        self, attack_anns, attacker, propagation_round
    ):
        """Set attack_anns to only the announcement with the shortest path"""
        # if the list was empty, the previous function would have returned
        # before calling this one, so it is not necessary to check here
        shortest_so_far = attack_anns[0]
        for ann in attack_anns:
            if len(ann.as_path) < len(shortest_so_far.as_path):
                shortest_so_far = ann
        attack_anns = [shortest_so_far]
        super().leak_announcements_to_providers(
            attack_anns, attacker, propagation_round
        )
