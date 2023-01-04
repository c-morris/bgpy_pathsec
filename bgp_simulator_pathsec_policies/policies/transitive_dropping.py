import random

from bgp_simulator_pkg import BGPAS


class TransitiveDroppingAS(BGPAS):
    """Drops transitive attributes with some probability"""
    name = "TransitiveDroppingAS"
    transitive_dropping_percent=1.0

    def __init__(self,
                 *args,
                 **kwargs):
        # Set the probability of dropping transitive attrs for *this* AS only
        self.transitive_dropping = (
            random.random() < (self.transitive_dropping_percent / 100.0))

        super(TransitiveDroppingAS, self).__init__(*args,
                                                   **kwargs)
    def _process_outgoing_ann(self, as_obj, ann, propagate_to, send_rels, *args, **kwargs): # noqa E501
        """If this is a transitive dropping AS, drop transitive attributes"""
        ann_to_send = ann.copy()
        if self.transitive_dropping:
            ann_to_send.next_as = 0
            ann_to_send.do_communities = tuple()
            # The signatures removed, if any, will be detected by adopting ASes
            ann_to_send.removed_signatures = ann_to_send.bgpsec_path
            ann_to_send.bgpsec_path = tuple()
        super(TransitiveDroppingAS, self)._process_outgoing_ann(as_obj, ann_to_send, propagate_to, send_rels, *args, **kwargs) # noqa E501

class TransitiveDropping2AS(TransitiveDroppingAS):
    """Drops transitive attributes with some probability"""
    name = "TransitiveDropping2AS"
    transitive_dropping_percent=2.0

class TransitiveDropping4AS(TransitiveDroppingAS):
    """Drops transitive attributes with some probability"""
    name = "TransitiveDropping4AS"
    transitive_dropping_percent=4.0

class TransitiveDropping8AS(TransitiveDroppingAS):
    """Drops transitive attributes with some probability"""
    name = "TransitiveDropping8AS"
    transitive_dropping_percent=8.0

class TransitiveDropping16AS(TransitiveDroppingAS):
    """Drops transitive attributes with some probability"""
    name = "TransitiveDropping16AS"
    transitive_dropping_percent=16.0

class TransitiveDropping32AS(TransitiveDroppingAS):
    """Drops transitive attributes with some probability"""
    name = "TransitiveDropping32AS"
    transitive_dropping_percent=32.0

class TransitiveDropping64AS(TransitiveDroppingAS):
    """Drops transitive attributes with some probability"""
    name = "TransitiveDropping64AS"
    transitive_dropping_percent=64.0
