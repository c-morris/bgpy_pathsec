
from lib_bgp_simulator import Relationships, BGPRIBSPolicy, BGPAS

from bgp_simulator_policies import PAnn, DownOnlyPolicy

def test_process_incoming_anns_do():
    """Test basic functionality of process_incoming_anns"""
    prefix = '137.99.0.0/16'
    ann = PAnn(prefix=prefix, as_path=(13796,),timestamp=0)
    a = BGPAS(1) 
    a.policy = DownOnlyPolicy()
    a.policy.recv_q[13796][prefix].append(ann)
    a.policy.process_incoming_anns(a, Relationships.CUSTOMERS)
    # assert announcement was accepted to local rib
    assert(a.policy.local_rib[prefix].origin == ann.origin)

def test_process_incoming_anns_do_reject():
    """Test basic functionality of process_incoming_anns"""
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
    """Test basic functionality of process_incoming_anns"""
    prefix = '137.99.0.0/16'
    ann = PAnn(prefix=prefix, as_path=(13796,),timestamp=0)
    ann.do_communities = (13796,)
    a = BGPAS(1) 
    a.policy = DownOnlyPolicy()
    a.policy.recv_q[13796][prefix].append(ann)
    a.policy.process_incoming_anns(a, Relationships.PROVIDERS)
    # assert announcement was accepted to local rib
    assert(a.policy.local_rib[prefix].origin == ann.origin)

def test_populate_send_q_do():
    """Test basic functionality of process_incoming_anns"""
    prefix = '137.99.0.0/16'
    ann = PAnn(prefix=prefix, as_path=(13796,),timestamp=0)
    a = BGPAS(1) 
    b = BGPAS(2)
    a.policy = DownOnlyPolicy()
    b.policy = DownOnlyPolicy()
    a.customers = [b]
    a.policy.recv_q[13796][prefix].append(ann)
    a.policy.process_incoming_anns(a, Relationships.CUSTOMERS)
    a.policy._populate_send_q(a, Relationships.CUSTOMERS, [Relationships.CUSTOMERS])
    assert(a.policy.send_q[2][prefix][0].do_communities == (1,))



