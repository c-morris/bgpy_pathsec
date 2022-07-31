from lib_caida_collector import PeerLink, CustomerProviderLink as CPLink

from lib_bgp_simulator import GraphInfo


class PGraph001(GraphInfo):
    r"""
      1
     / \
    2   3
     \  |
      \ 4
       \|
       777--666
    """
    def __init__(self):
        # Graph data
        peers = [PeerLink(777, 666)]
        customer_providers = [CPLink(provider_asn=1, customer_asn=2),
                              CPLink(provider_asn=1, customer_asn=3),
                              CPLink(provider_asn=2, customer_asn=777),
                              CPLink(provider_asn=3, customer_asn=4),
                              CPLink(provider_asn=4, customer_asn=777)]
        super(PGraph001, self).__init__(
            peer_links=set(peers),
            customer_provider_links=set(customer_providers))
