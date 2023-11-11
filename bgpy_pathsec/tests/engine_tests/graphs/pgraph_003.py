from bgpy.caida_collector import PeerLink, CustomerProviderLink as CPLink
from bgpy import GraphInfo

r"""
  1
 / \
2---3
|   |
4  777---666---5
"""

p_graph_003 = GraphInfo(
    peer_links=set([PeerLink(777, 666), PeerLink(666, 5)]),
    customer_provider_links=set(
        [
            CPLink(provider_asn=1, customer_asn=2),
            CPLink(provider_asn=1, customer_asn=3),
            CPLink(provider_asn=2, customer_asn=4),
            CPLink(provider_asn=3, customer_asn=777),
        ]
    ),
)
