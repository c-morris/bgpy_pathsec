from .ris_neighbors import ris_neighbors
from .eavesdropper import Eavesdropper

class RISEavesdropper(Eavesdropper):
    """Attacker has visibility into RIS collectors.
    """
    vantage_points = ris_neighbors

