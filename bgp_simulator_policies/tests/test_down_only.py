import pytest

from lib_caida_collector import PeerLink, CustomerProviderLink as CPLink
from lib_bgp_simulator import Relationships, BGPRIBSPolicy, BGPAS, Relationships, LocalRib, run_example

from bgp_simulator_policies import PAnn, DownOnlyPolicy, BGPsecPolicy, BGPsecTransitiveDownOnlyPolicy

def test_process_incoming_anns_do_reject():
    """Test rejection of ann from customer with DO community"""
    prefix = '137.99.0.0/16'
    ann = PAnn(prefix=prefix, as_path=(13796,),timestamp=0, recv_relationship=Relationships.ORIGIN)
    ann.do_communities = (13796,)
    a = BGPAS(1) 
    a.policy = DownOnlyPolicy()
    a.policy.recv_q[13796][prefix].append(ann)
    a.policy.process_incoming_anns(a, Relationships.CUSTOMERS)
    # assert announcement was accepted to local rib
    assert(a.policy.local_rib.get(prefix) is None)

def test_process_incoming_anns_do_accept():
    """Test acceptance of ann from non-customer with DO community"""
    prefix = '137.99.0.0/16'
    ann = PAnn(prefix=prefix, as_path=(13796,),timestamp=0, recv_relationship=Relationships.ORIGIN)
    ann.do_communities = (13796,)
    a = BGPAS(1) 
    a.policy = DownOnlyPolicy()
    a.policy.recv_q[13796][prefix].append(ann)
    a.policy.process_incoming_anns(a, Relationships.PROVIDERS)
    # assert announcement was accepted to local rib
    assert(a.policy.local_rib[prefix].origin == ann.origin)

@pytest.mark.parametrize("b_relationship, community_len", [[Relationships.CUSTOMERS, 1],
                                                           [Relationships.PROVIDERS, 0]])
def test_populate_send_q_do(b_relationship, community_len):
    """Test addition of DO community when propagating to customers"""
    prefix = '137.99.0.0/16'
    ann = PAnn(prefix=prefix, as_path=(13796,),timestamp=0, recv_relationship=Relationships.ORIGIN)
    a = BGPAS(1) 
    b = BGPAS(2)
    a.policy = DownOnlyPolicy()
    b.policy = DownOnlyPolicy()
    setattr(a, b_relationship.name.lower(), (b,))
    a.policy.recv_q[13796][prefix].append(ann)
    a.policy.process_incoming_anns(a, Relationships.CUSTOMERS)
    a.policy._populate_send_q(a, b_relationship, [Relationships.CUSTOMERS])
    assert(len(a.policy.send_q[2][prefix][0].do_communities) == community_len)

@pytest.mark.parametrize("BasePolicyCls", [DownOnlyPolicy, BGPsecTransitiveDownOnlyPolicy])
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
    announcements = [PAnn(prefix=prefix, as_path=(5,),timestamp=0, seed_asn=5,
                                  do_communities = tuple(),
                                  bgpsec_path=(5,),
                                  next_as=5,
                                  recv_relationship=Relationships.ORIGIN,
                                  traceback_end=True)]

    kwargs = {"prefix": prefix, "timestamp": 0,
                      "traceback_end": False}

    # Local RIB data
    local_ribs = {
        1: LocalRib({prefix: PAnn(as_path=(1, 3, 5), do_communities=tuple(), recv_relationship=Relationships.CUSTOMERS, **kwargs)}),
        2: LocalRib({prefix: PAnn(as_path=(2, 3, 5), do_communities=(3,), recv_relationship=Relationships.PEERS, **kwargs)}),
        3: LocalRib({prefix: PAnn(as_path=(3, 5), do_communities=tuple(), recv_relationship=Relationships.CUSTOMERS, **kwargs)}),
        4: LocalRib({prefix: PAnn(as_path=(4, 2, 3, 5), do_communities=(2, 3), recv_relationship=Relationships.PROVIDERS, **kwargs)}),
        5: LocalRib({prefix: announcements[0]}),
    }

    run_example(peers=peers,
                customer_providers=customer_providers,
                as_policies=as_policies,
                announcements=announcements,
                local_ribs=local_ribs)
