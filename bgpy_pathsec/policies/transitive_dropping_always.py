from .transitive_dropping import TransitiveDroppingAS


class TransitiveDroppingAlwaysAS(TransitiveDroppingAS):
    """Drops transitive attributes with some probability"""

    name = "TransitiveDroppingAlwaysAS"

    def __init__(self, *args, transitive_dropping_percent=1.0, **kwargs):
        # Set the probability of dropping transitive attrs for *this* AS only
        # For this test class, this is always true
        self.transitive_dropping = True

        super(TransitiveDroppingAS, self).__init__(*args, **kwargs)
