from bgp_simulator_pkg import Prefixes, Relationships

from .shortest_path_export_all_no_hash import ShortestPathExportAllNoHash


class GlobalEavesdropper(Eavesdropper):
    """Attacker has visibility into all other AS RIBs.
    """

    global_eavesdropper = True
