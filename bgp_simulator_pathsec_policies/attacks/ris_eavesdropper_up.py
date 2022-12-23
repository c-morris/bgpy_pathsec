from .ris_neighbors import ris_neighbors
from .eavesdropper_up import EavesdropperUp


class RISEavesdropperUp(EavesdropperUp):
    """Attacker has visibility into RIS collectors.
       This version assumes UP attributes.
    """
    vantage_points = ris_neighbors
