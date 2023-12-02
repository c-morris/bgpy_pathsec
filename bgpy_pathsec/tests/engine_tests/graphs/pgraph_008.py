from bgpy.caida_collector import PeerLink, CustomerProviderLink as CPLink
from bgpy import GraphInfo

r"""
      1------6---7
     / \    /|    \
    2   |  8 |    777
    |   |   \|
    3---4    9
     \ /    /
      5    /
       \  /
        666
"""

p_graph_008 = GraphInfo(
    peer_links=set(
        [
            PeerLink(1, 6),
            PeerLink(3, 4),
            PeerLink(6, 7),
            PeerLink(1, 7),
        ]
    ),
    customer_provider_links=set(
        [
            CPLink(provider_asn=1, customer_asn=2),
            CPLink(provider_asn=1, customer_asn=4),
            CPLink(provider_asn=2, customer_asn=3),
            CPLink(provider_asn=4, customer_asn=5),
            CPLink(provider_asn=3, customer_asn=5),
            CPLink(provider_asn=6, customer_asn=8),
            CPLink(provider_asn=6, customer_asn=9),
            CPLink(provider_asn=8, customer_asn=9),
            CPLink(provider_asn=7, customer_asn=777),
            CPLink(provider_asn=5, customer_asn=666),
            CPLink(provider_asn=9, customer_asn=666),
        ]
    ),
)
