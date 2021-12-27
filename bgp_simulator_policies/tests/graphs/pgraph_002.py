from lib_caida_collector import PeerLink, CustomerProviderLink as CPLink

from lib_bgp_simulator import GraphInfo


class PGraph002(GraphInfo):
    r"""
    Test BGPsec transitive preference for fewer nonadopting segments.
    Horizontal lines are peer relationships, vertical lines are
    customer-provider.

      1
     / \
    2   3
    |   |
    6   7
    |   |
    8   9
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
                              CPLink(provider_asn=2, customer_asn=6),
                              CPLink(provider_asn=3, customer_asn=7),
                              CPLink(provider_asn=4, customer_asn=777),
                              CPLink(provider_asn=6, customer_asn=8),
                              CPLink(provider_asn=7, customer_asn=9),
                              CPLink(provider_asn=8, customer_asn=777),
                              CPLink(provider_asn=9, customer_asn=4),
                              ]

        super(PGraph002, self).__init__(
            peer_links=set(peers),
            customer_provider_links=set(customer_providers))
