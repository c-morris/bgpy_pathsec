from bgpy.caida_collector import PeerLink, CustomerProviderLink as CPLink

from bgpy import GraphInfo

r"""
  1
 / \
2   3
 \  |
  5 4
   \|
   777--666
"""


p_graph_001 = GraphInfo(
    peer_links = set([PeerLink(777, 666)]),
    customer_provider_links = set(
        [
           CPLink(provider_asn=1, customer_asn=2),
           CPLink(provider_asn=1, customer_asn=3),
           CPLink(provider_asn=2, customer_asn=5),
           CPLink(provider_asn=5, customer_asn=777),
           CPLink(provider_asn=3, customer_asn=4),
           CPLink(provider_asn=4, customer_asn=777),
        ]
    )
)

