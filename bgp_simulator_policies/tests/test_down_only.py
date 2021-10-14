import pytest

from lib_caida_collector import PeerLink, CustomerProviderLink as CPLink
from lib_bgp_simulator import Relationships, BGPRIBsAS, BGPAS, Relationships, LocalRib, run_example

from bgp_simulator_policies import PTestAnn, DownOnlyAS, BGPsecAS, BGPsecTransitiveDownOnlyAS

def test_process_incoming_anns_do_reject():
    """Test rejection of ann from customer with DO community"""
    prefix = '137.99.0.0/16'
    ann = PTestAnn(prefix=prefix, as_path=(13796,),timestamp=0, recv_relationship=Relationships.ORIGIN)
    ann.do_communities = (13796,)
    a = DownOnlyAS(1)
    a._recv_q.add_ann(ann)
    a.process_incoming_anns(Relationships.CUSTOMERS)
    # assert announcement was accepted to local rib
    assert(a._local_rib.get_ann(prefix) is None)

def test_process_incoming_anns_do_accept():
    """Test acceptance of ann from non-customer with DO community"""
    prefix = '137.99.0.0/16'
    ann = PTestAnn(prefix=prefix, as_path=(13796,),timestamp=0, recv_relationship=Relationships.ORIGIN)
    ann.do_communities = (13796,)
    a = DownOnlyAS(1)
    a._recv_q.add_ann(ann)
    a.process_incoming_anns(Relationships.PROVIDERS)
    # assert announcement was accepted to local rib
    assert(a._local_rib.get_ann(prefix).origin == ann.origin)

@pytest.mark.parametrize("b_relationship, community_len", [[Relationships.CUSTOMERS, 1],
                                                           [Relationships.PROVIDERS, 0]])
def test_populate_send_q_do(b_relationship, community_len):
    """Test addition of DO community when propagating to customers"""
    prefix = '137.99.0.0/16'
    ann = PTestAnn(prefix=prefix, as_path=(13796,),timestamp=0, recv_relationship=Relationships.ORIGIN)
    a = DownOnlyAS(1)
    b = DownOnlyAS(2)
    setattr(a, b_relationship.name.lower(), (b,))
    a._recv_q.add_ann(ann)
    a.process_incoming_anns(Relationships.CUSTOMERS)
    a._populate_send_q(b_relationship, [Relationships.CUSTOMERS])
    assert(len(a._send_q.get_send_info(b, prefix).ann.do_communities) == community_len)

@pytest.mark.parametrize("BasePolicyCls", [DownOnlyAS, BGPsecTransitiveDownOnlyAS])
def test_propagate_do(BasePolicyCls):
    r"""
    Test the setting of down-only communities.
    Horizontal lines are peer relationships, vertical lines are customer-provider. 
                                                                             
      1                                                                         
     / \                                                                         
    2---3                                                                     
    |   |                                                                    
    4   5                                                                  
        
    Starting propagation at 5.
    """
    # Graph data
    peers = [PeerLink(2, 3)]
    customer_providers = [CPLink(provider_asn=1, customer_asn=2),
                          CPLink(provider_asn=1, customer_asn=3),
                          CPLink(provider_asn=2, customer_asn=4),
                          CPLink(provider_asn=3, customer_asn=5)]
    # Number identifying the type of AS class
    as_policies = {asn: BasePolicyCls for asn in
                   list(range(1, 6))}

    # Announcements
    prefix = '137.99.0.0/16'
    announcements = [PTestAnn(prefix=prefix, as_path=(5,),timestamp=0, seed_asn=5,
                                  do_communities = tuple(),
                                  bgpsec_path=(5,),
                                  next_as=5,
                                  recv_relationship=Relationships.ORIGIN,
                                  traceback_end=True)]

    kwargs = {"prefix": prefix, "timestamp": 0,
                      "traceback_end": False}

    # Local RIB data
    _local_ribs = {
        1: {prefix: PTestAnn(as_path=(1, 3, 5), do_communities=tuple(), recv_relationship=Relationships.CUSTOMERS, **kwargs)},
        2: {prefix: PTestAnn(as_path=(2, 3, 5), do_communities=(3,), recv_relationship=Relationships.PEERS, **kwargs)},
        3: {prefix: PTestAnn(as_path=(3, 5), do_communities=tuple(), recv_relationship=Relationships.CUSTOMERS, **kwargs)},
        4: {prefix: PTestAnn(as_path=(4, 2, 3, 5), do_communities=(2, 3), recv_relationship=Relationships.PROVIDERS, **kwargs)},
        5: {prefix: announcements[0]},
    }

    run_example(peers=peers,
                customer_providers=customer_providers,
                as_policies=as_policies,
                announcements=announcements,
                local_ribs=_local_ribs)
