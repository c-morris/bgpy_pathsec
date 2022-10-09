from .ris_neighbors import ris_neighbors
from .eavesdropper import Eavesdropper

class RISEavesdropperUp(Eavesdropper):
    """Attacker has visibility into RIS collectors.
       This version assumes UP attributes.
    """
    vantage_points = ris_neighbors

