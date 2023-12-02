from bgpy.caida_collector import CustomerProviderLink as CPLink
from bgpy import GraphInfo

r"""
  4
 / \
7   6
|\  |
2 5 666
|  \|
777  3
"""

p_graph_009 = GraphInfo(
    peer_links=set([]),
    customer_provider_links=set(
        [
            CPLink(provider_asn=4, customer_asn=7),
            CPLink(provider_asn=4, customer_asn=6),
            CPLink(provider_asn=7, customer_asn=5),
            CPLink(provider_asn=5, customer_asn=3),
            CPLink(provider_asn=7, customer_asn=2),
            CPLink(provider_asn=2, customer_asn=777),
            CPLink(provider_asn=666, customer_asn=3),
            CPLink(provider_asn=6, customer_asn=666),
        ]
    ),
)
