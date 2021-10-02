import pytest

from lib_caida_collector import PeerLink, CustomerProviderLink as CPLink
from lib_bgp_simulator import Relationships, BGPRIBSPolicy, BGPAS, Relationships, LocalRib, run_example

from bgp_simulator_policies import PAnn, DownOnlyPolicy, BGPsecPolicy

# In BGPsec, an attacker should never send an invalid signature. It is always
# more advantageous to strip the security attributes and send a legacy
# announcement, which will likely be depreferred, but should not be rejected
# outright. 

def test_process_incoming_anns_bgpsec_depref():
    """Test preference of ann from customer with a BGPsec signature"""
    prefix = '137.99.0.0/16'
    ann1 = PAnn(prefix=prefix, as_path=(13796,),timestamp=0, recv_relationship=Relationships.ORIGIN)
    ann2 = PAnn(prefix=prefix, as_path=(13795,),timestamp=0, recv_relationship=Relationships.ORIGIN)
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

def test_bgpsec_update_attrs():
    """Test updating of bgpsec attributes when forwarding a bgpsec ann"""
    prefix = '137.99.0.0/16'
    ann = PAnn(prefix=prefix, as_path=(13796,),timestamp=0, recv_relationship=Relationships.ORIGIN)
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

def test_bgpsec_remove_attrs():
    """Test removal of bgpsec attributes when a non-adopting AS is detected on the path"""
    prefix = '137.99.0.0/16'
    ann = PAnn(prefix=prefix, as_path=(13795, 13796),timestamp=0, recv_relationship=Relationships.ORIGIN)
    ann.bgpsec_path = (13796)
    ann.next_as = 13795
    a = BGPAS(1) 
    b = BGPAS(2)
    a.customers = [b]
    a.policy = BGPsecPolicy()
    b.policy = BGPsecPolicy()
    a.policy.recv_q[13796][prefix].append(ann)
    a.policy.process_incoming_anns(a, Relationships.CUSTOMERS)
    a.policy._populate_send_q(a, Relationships.CUSTOMERS, [Relationships.CUSTOMERS])
    assert(len(a.policy.send_q[2][prefix][0].bgpsec_path) == 0 and 
           a.policy.send_q[2][prefix][0].next_as == 0)

@pytest.mark.parametrize("BasePolicyCls", [BGPsecPolicy])
def test_propagate_bgp(BasePolicyCls):
    r"""
    Test BGPsec preference for authenticated paths.
    Horizontal lines are peer relationships, vertical lines are customer-provider. 
                                                                             
      1                                                                         
     / \                                                                         
    2   3                                                                     
     \  |                                                                    
      \ 4                                                                  
       \|
        5
    Starting propagation at 5, the longer path through adopting ASes should be preferred.
    """
    # Graph data
    peers = []
    customer_providers = [CPLink(provider_asn=1, customer_asn=2),
                          CPLink(provider_asn=1, customer_asn=3),
                          CPLink(provider_asn=2, customer_asn=5),
                          CPLink(provider_asn=3, customer_asn=4),
                          CPLink(provider_asn=4, customer_asn=5)]
    # Number identifying the type of AS class
    as_policies = {asn: BasePolicyCls for asn in
                   list(range(1, 6))}
    as_policies[2] = BGPRIBSPolicy

    # Announcements
    prefix = '137.99.0.0/16'
    announcements = [PAnn(prefix=prefix, as_path=(5,),timestamp=0, seed_asn=5,
                                  bgpsec_path=(5,),
                                  next_as=5,
                                  recv_relationship=Relationships.ORIGIN,
                                  traceback_end=True)]

    kwargs = {"prefix": prefix, "timestamp": 0,
                      "traceback_end": False}

    # Local RIB data
    local_ribs = {
        1: LocalRib({prefix: PAnn(as_path=(1, 3, 4, 5), bgpsec_path=(1, 3, 4, 5), next_as=1, recv_relationship=Relationships.CUSTOMERS, **kwargs)}),
        2: LocalRib({prefix: PAnn(as_path=(2, 5), bgpsec_path=(5,), next_as=5, recv_relationship=Relationships.CUSTOMERS, **kwargs)}),
        3: LocalRib({prefix: PAnn(as_path=(3, 4, 5), bgpsec_path=(3, 4, 5), next_as=3, recv_relationship=Relationships.CUSTOMERS, **kwargs)}),
        4: LocalRib({prefix: PAnn(as_path=(4, 5), bgpsec_path=(4, 5), next_as=4, recv_relationship=Relationships.CUSTOMERS, **kwargs)}),
        5: LocalRib({prefix: announcements[0]}),
    }

    run_example(peers=peers,
                customer_providers=customer_providers,
                as_policies=as_policies,
                announcements=announcements,
                local_ribs=local_ribs)
