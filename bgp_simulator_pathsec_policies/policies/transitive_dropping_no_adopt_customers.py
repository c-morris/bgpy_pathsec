from .transitive_dropping import TransitiveDroppingAS, TransitiveDroppingNeverAS

from bgp_simulator_pkg import Relationships


class TransitiveDroppingNoAdoptCustomersAS(TransitiveDroppingAS):
    """Drops transitive attributes with some probability.

    Ensures no customers are adopting ASes.

    Do not run this in a simulation with other scenarios, it breaks them.
    """

    name = "TransitiveDroppingNoAdoptCustomersAS"
    convert_count = 0

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
                        as_.transitive_dropping = False
                        TransitiveDroppingNoAdoptCustomersAS.convert_count += 1
                        
        super().propagate_to_customers()

class TransitiveDroppingNoAdoptCustomersAlwaysAS(TransitiveDroppingNoAdoptCustomersAS):
    """Drops transitive attributes with some probability"""
    name = "TransitiveDroppingNoAdoptCustomersAlwaysAS"
    transitive_dropping_percent = 100.0


class TransitiveDroppingNoAdoptCustomers2AS(TransitiveDroppingNoAdoptCustomersAS):
    """Drops transitive attributes with some probability"""
    name = "TransitiveDroppingNoAdoptCustomers2AS"
    transitive_dropping_percent=2.0


class TransitiveDroppingNoAdoptCustomers4AS(TransitiveDroppingNoAdoptCustomersAS):
    """Drops transitive attributes with some probability"""
    name = "TransitiveDroppingNoAdoptCustomers4AS"
    transitive_dropping_percent=4.0

