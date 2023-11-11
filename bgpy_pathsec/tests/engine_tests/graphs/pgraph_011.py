from bgpy.caida_collector import PeerLink, CustomerProviderLink as CPLink
from bgpy import GraphInfo

r"""
  3
 / \
2   5
|   |\
1   4 \
|\  |  10
6 | 9
/  |/
7  777--666

Professor Wang's recommended transitive dropping test case.
"""

p_graph_011 = GraphInfo(
    peer_links=set([PeerLink(777, 666)]),
    customer_provider_links=set(
        [
            CPLink(provider_asn=3, customer_asn=2),
            CPLink(provider_asn=3, customer_asn=5),
            CPLink(provider_asn=2, customer_asn=1),
            CPLink(provider_asn=5, customer_asn=4),
            CPLink(provider_asn=5, customer_asn=10),
            CPLink(provider_asn=1, customer_asn=6),
            CPLink(provider_asn=1, customer_asn=777),
            CPLink(provider_asn=4, customer_asn=9),
            CPLink(provider_asn=6, customer_asn=7),
            CPLink(provider_asn=9, customer_asn=777),
        ]
    ),
)
