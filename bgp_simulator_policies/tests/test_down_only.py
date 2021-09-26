import pytest

from lib_bgp_simulator import Relationships, BGPRIBSPolicy, BGPAS

from bgp_simulator_policies import PAnn, DownOnlyPolicy, BGPsecPolicy

def test_process_incoming_anns_do_reject():
    """Test rejection of ann from customer with DO community"""
    prefix = '137.99.0.0/16'
    ann = PAnn(prefix=prefix, as_path=(13796,),timestamp=0)
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
    ann = PAnn(prefix=prefix, as_path=(13796,),timestamp=0)
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
    ann = PAnn(prefix=prefix, as_path=(13796,),timestamp=0)
    a = BGPAS(1) 
    b = BGPAS(2)
    a.policy = DownOnlyPolicy()
    b.policy = DownOnlyPolicy()
    setattr(a, b_relationship.name.lower(), (b,))
    a.policy.recv_q[13796][prefix].append(ann)
    a.policy.process_incoming_anns(a, Relationships.CUSTOMERS)
    a.policy._populate_send_q(a, b_relationship, [Relationships.CUSTOMERS])
    assert(len(a.policy.send_q[2][prefix][0].do_communities) == community_len)

