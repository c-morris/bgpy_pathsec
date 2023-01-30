from .transitive_dropping import TransitiveDroppingAS, TransitiveDroppingNeverAS

from bgp_simulator_pkg import Relationships, Prefixes


class TransitiveDroppingNoAdoptCustomersAS(TransitiveDroppingAS):
    """Drops transitive attributes with some probability.

    Ensures no customers are adopting ASes.

    Do not run this in a simulation with other scenarios, it breaks them.
    """

    name = "TransitiveDroppingNoAdoptCustomersAS"
    convert_count = 0

    def propagate_to_customers(self):
        """After sending, switch customer to BGPAS if necessary."""

        super().propagate_to_customers()
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
                    if origin:
                        # If the origin is a customer, don't drop attrs 
                        self.transitive_dropping = False
                    else:
                        as_.__class__ = TransitiveDroppingNeverAS
                        as_.transitive_dropping = False
                        best_ann = as_._select_best_ribs_in(Prefixes.PREFIX.value)
                        # Re-process ribs_in with new AS class
                        current_ann = as_._local_rib.get_ann(Prefixes.PREFIX.value)
                        if best_ann is not None and not best_ann.prefix_path_attributes_eq(current_ann):
                            if current_ann is not None:
                                withdraw_ann = current_ann.copy(
                                    overwrite_default_kwargs={'withdraw': True})
                                as_._local_rib.remove_ann(Prefixes.PREFIX.value)
                                # Also remove from neighbors
                                as_._withdraw_ann_from_neighbors(withdraw_ann)
                            # Add new best ann to local RIB
                            as_._local_rib.add_ann(best_ann)
                        TransitiveDroppingNoAdoptCustomersAS.convert_count += 1

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

