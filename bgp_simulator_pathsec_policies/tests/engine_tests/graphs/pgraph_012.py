from caida_collector_pkg import CustomerProviderLink as CPLink

from bgpy import GraphInfo


class PGraph012(GraphInfo):
    r"""
      4
     / \
    7   6
    |\  |
 8  2 5 666
  \ |  \|
   777  3
    """
    def __init__(self):
        # Graph data
        peers = []
        customer_providers = [CPLink(provider_asn=4, customer_asn=7),
                              CPLink(provider_asn=4, customer_asn=6),
                              CPLink(provider_asn=7, customer_asn=5),
                              CPLink(provider_asn=5, customer_asn=3),
                              CPLink(provider_asn=7, customer_asn=2),
                              CPLink(provider_asn=2, customer_asn=777),
                              CPLink(provider_asn=8, customer_asn=777),
                              CPLink(provider_asn=666, customer_asn=3),
                              CPLink(provider_asn=6, customer_asn=666)]
        super(PGraph012, self).__init__(
            peer_links=set(peers),
            customer_provider_links=set(customer_providers))
