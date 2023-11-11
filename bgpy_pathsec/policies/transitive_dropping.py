import random

from bgpy import BGPAS


class TransitiveDroppingAS(BGPAS):
    """Drops transitive attributes with some probability"""

    name = "TransitiveDroppingAS"
    count = 0
    bpo_count = 0
    transitive_dropping_percent = 1.0
    # Specific random generator for TransitiveDroppingAS and its subclasses
    # for reproduceable experiments
    rand_gen = random.Random("TransitiveDroppingAS")

    def __init__(self, *args, **kwargs):
        # Set the probability of dropping transitive attrs for *this* AS only
        self.transitive_dropping = self.rand_gen.random() < (
            self.transitive_dropping_percent / 100.0
        )

        super(TransitiveDroppingAS, self).__init__(*args, **kwargs)

    def _process_outgoing_ann(
        self, as_obj, ann, propagate_to, send_rels, *args, **kwargs
    ):
        """If this is a transitive dropping AS, drop transitive attributes"""
        ann_to_send = ann
        if self.transitive_dropping:
            ann_to_send = replace(ann_to_send,
                next_as = 0,
                do_communities = tuple(),
            )
            # The signatures removed, if any, will be detected by adopting ASes
            if len(ann_to_send.removed_signatures) == 0:
                ann_to_send = replace(ann_to_send, removed_signatures = ann_to_send.bgpsec_path)
            ann_to_send = replace(ann_to_send, bgpsec_path = tuple())
        super(TransitiveDroppingAS, self)._process_outgoing_ann(
            as_obj, ann_to_send, propagate_to, send_rels, *args, **kwargs
        )


class TransitiveDropping2AS(TransitiveDroppingAS):
    """Drops transitive attributes with some probability"""

    name = "TransitiveDropping2AS"
    transitive_dropping_percent = 2.0


class TransitiveDropping4AS(TransitiveDroppingAS):
    """Drops transitive attributes with some probability"""

    name = "TransitiveDropping4AS"
    transitive_dropping_percent = 4.0


class TransitiveDropping8AS(TransitiveDroppingAS):
    """Drops transitive attributes with some probability"""

    name = "TransitiveDropping8AS"
    transitive_dropping_percent = 8.0


class TransitiveDropping16AS(TransitiveDroppingAS):
    """Drops transitive attributes with some probability"""

    name = "TransitiveDropping16AS"
    transitive_dropping_percent = 16.0


class TransitiveDropping32AS(TransitiveDroppingAS):
    """Drops transitive attributes with some probability"""

    name = "TransitiveDropping32AS"
    transitive_dropping_percent = 32.0


class TransitiveDropping64AS(TransitiveDroppingAS):
    """Drops transitive attributes with some probability"""

    name = "TransitiveDropping64AS"
    transitive_dropping_percent = 64.0


class TransitiveDropping99AS(TransitiveDroppingAS):
    """Drops transitive attributes with some probability"""

    name = "TransitiveDropping99AS"
    transitive_dropping_percent = 99.0


class TransitiveDroppingNeverAS(TransitiveDroppingAS):
    """Drops transitive attributes with some probability"""

    name = "TransitiveDroppingNeverAS"
    transitive_dropping_percent = 0.0
