from .transitive_dropping import TransitiveDroppingAS, TransitiveDroppingNeverAS


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
            print('gawt here')
            for as_ in self.customers:
                #if not (isinstance(as_, TransitiveDroppingAS) or
                #        isinstance(as_, BGPAS)):
                    print(isinstance(as_, TransitiveDroppingAS))
                    as_.__class__ = TransitiveDroppingNeverAS
                    #as_.__init__(reset_base=False)
                    print('got here', as_.asn)
        super().propagate_to_customers()

class TransitiveDroppingNoAdoptCustomersAlwaysAS(TransitiveDroppingNoAdoptCustomersAS):

    name = "TransitiveDroppingNoAdoptCustomersAlwaysAS"
    transitive_dropping_percent = 100.0

