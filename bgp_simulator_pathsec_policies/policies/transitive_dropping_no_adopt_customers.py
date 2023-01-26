from .transitive_dropping import TransitiveDroppingAS, TransitiveDroppingNeverAS

from bgp_simulator_pkg import Relationships


class TransitiveDroppingNoAdoptCustomersAS(TransitiveDroppingAS):
    """Drops transitive attributes with some probability.

    Ensures no customers are adopting ASes.

    Do not run this in a simulation with other scenarios, it breaks them.
    """

    name = "TransitiveDroppingNoAdoptCustomersAS"

    def propagate_to_customers(self):
        """Before sending, switch customer to BGPAS if necessary."""

        # If this is a transitive dropping AS, switch all adopting customers
        # to non-adopting. 
        if self.transitive_dropping:
            for as_ in self.customers:
                if not (isinstance(as_, TransitiveDroppingAS)):
                    # The origin must stay adopting
                    origin = False
                    for prefix, ann in as_._local_rib.prefix_anns():
                        if ann.recv_relationship == Relationships.ORIGIN:
                            origin = True
                    if not origin:
                        as_.__class__ = TransitiveDroppingNeverAS
        super().propagate_to_customers()

class TransitiveDroppingNoAdoptCustomersAlwaysAS(TransitiveDroppingNoAdoptCustomersAS):

    name = "TransitiveDroppingNoAdoptCustomersAlwaysAS"
    transitive_dropping_percent = 100.0

