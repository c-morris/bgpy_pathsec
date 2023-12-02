# New way
from bgpy.caida_collector import PeerLink, CustomerProviderLink as CPLink
from bgpy import GraphInfo

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
  5 4
   \|
   777--666
"""

p_graph_002 = GraphInfo(
    peer_links=set([PeerLink(777, 666)]),
    customer_provider_links=set(
        [
            CPLink(provider_asn=1, customer_asn=2),
            CPLink(provider_asn=1, customer_asn=3),
            CPLink(provider_asn=2, customer_asn=6),
            CPLink(provider_asn=3, customer_asn=7),
            CPLink(provider_asn=4, customer_asn=777),
            CPLink(provider_asn=6, customer_asn=8),
            CPLink(provider_asn=7, customer_asn=9),
            CPLink(provider_asn=8, customer_asn=5),
            CPLink(provider_asn=5, customer_asn=777),
            CPLink(provider_asn=9, customer_asn=4),
        ]
    ),
)
