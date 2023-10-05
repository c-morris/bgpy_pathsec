from caida_collector_pkg import PeerLink, CustomerProviderLink as CPLink

from bgpy import GraphInfo


class PGraph007(GraphInfo):
    r"""
          1------6---7
         / \    /|    \       12
        2   |  8 |     \     /
        |   |   \|      10--11--15
        3---4    9       |  |
         \ /    /       13--14--16
          5    /         |
           \  /         777
            666
    """
    def __init__(self):
        # Graph data
        peers = [PeerLink(1, 6),
                 PeerLink(3, 4),
                 PeerLink(6, 7),
                 PeerLink(1, 7),
                 PeerLink(10, 11),
                 PeerLink(11, 15),
                 PeerLink(13, 14),
                 PeerLink(14, 16)]
        customer_providers = [CPLink(provider_asn=1, customer_asn=2),
                              CPLink(provider_asn=1, customer_asn=4),
                              CPLink(provider_asn=2, customer_asn=3),
                              CPLink(provider_asn=4, customer_asn=5),
                              CPLink(provider_asn=3, customer_asn=5),
                              CPLink(provider_asn=6, customer_asn=8),
                              CPLink(provider_asn=6, customer_asn=9),
                              CPLink(provider_asn=8, customer_asn=9),
                              CPLink(provider_asn=7, customer_asn=10),
                              CPLink(provider_asn=5, customer_asn=666),
                              CPLink(provider_asn=9, customer_asn=666),
                              CPLink(provider_asn=10, customer_asn=13),
                              CPLink(provider_asn=11, customer_asn=14),
                              CPLink(provider_asn=12, customer_asn=11),
                              CPLink(provider_asn=13, customer_asn=777),
                              ]
        super(PGraph007, self).__init__(
            peer_links=set(peers),
            customer_provider_links=set(customer_providers))
