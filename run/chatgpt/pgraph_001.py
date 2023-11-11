Please convert the Python code I'm about to give you from the old way to the new way. I've included an example below, with the old way first, and the new way second


```
# Old way

from caida_collector_pkg import PeerLink, CustomerProviderLink as CPLink

from bgpy import GraphInfo


class PGraph001(GraphInfo):
    r"""
      1
     / \
    2   3
     \  |
      5 4
       \|
       777--666
    """

    def __init__(self):
        # Graph data
        peers = [PeerLink(777, 666)]
        customer_providers = [
            CPLink(provider_asn=1, customer_asn=2),
            CPLink(provider_asn=1, customer_asn=3),
            CPLink(provider_asn=2, customer_asn=5),
            CPLink(provider_asn=5, customer_asn=777),
            CPLink(provider_asn=3, customer_asn=4),
            CPLink(provider_asn=4, customer_asn=777),
        ]
        super(PGraph001, self).__init__(
            peer_links=set(peers),
            customer_provider_links=set(customer_providers),
        )
```

```
# New way
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
    peers_links = set([PeerLink(777, 666)])
    customer_providers_links = set(
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
```
