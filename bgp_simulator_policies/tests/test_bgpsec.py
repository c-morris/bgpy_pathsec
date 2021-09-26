import pytest

from lib_bgp_simulator import Relationships, BGPRIBSPolicy, BGPAS

from bgp_simulator_policies import PAnn, DownOnlyPolicy, BGPsecPolicy

# In BGPsec, an attacker should never send an invalid signature. It is always
# more advantageous to strip the security attributes and send a legacy
# announcement, which will likely be depreferred, but should not be rejected
# outright. 

def test_process_incoming_anns_bgpsec_depref():
    """Test preference of ann from customer with a BGPsec signature"""
    prefix = '137.99.0.0/16'
    ann1 = PAnn(prefix=prefix, as_path=(13796,),timestamp=0)
    ann2 = PAnn(prefix=prefix, as_path=(13795,),timestamp=0)
    ann2.bgpsec_path = ann2.as_path
    ann2.next_as = 1
    a = BGPAS(1) 
    a.policy = BGPsecPolicy()
    a.policy.recv_q[13796][prefix].append(ann1)
    a.policy.process_incoming_anns(a, Relationships.CUSTOMERS)
    # assert announcement was accepted to local rib
    assert(a.policy.local_rib[prefix].origin == ann1.origin)
    # Now add announcement with valid signatures
    a.policy.recv_q[13795][prefix].append(ann2)
    a.policy.process_incoming_anns(a, Relationships.CUSTOMERS)
    # assert new announcement was accepted to local rib
    assert(a.policy.local_rib[prefix].origin == ann2.origin)

def test_process_incoming_anns_bgpsec_update_attrs():
    """Test updating of bgpsec attributes when forwarding a bgpsec ann"""
    prefix = '137.99.0.0/16'
    ann = PAnn(prefix=prefix, as_path=(13796,),timestamp=0)
    ann.bgpsec_path = ann.as_path
    ann.next_as = 1
    a = BGPAS(1) 
    b = BGPAS(2)
    a.customers = [b]
    a.policy = BGPsecPolicy()
    b.policy = BGPsecPolicy()
    a.policy.recv_q[13796][prefix].append(ann)
    a.policy.process_incoming_anns(a, Relationships.CUSTOMERS)
    a.policy._populate_send_q(a, Relationships.CUSTOMERS, [Relationships.CUSTOMERS])
    assert(a.policy.send_q[2][prefix][0].bgpsec_path == (1, 13796) and 
           a.policy.send_q[2][prefix][0].next_as == 2)
