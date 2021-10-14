import pytest

from lib_caida_collector import PeerLink, CustomerProviderLink as CPLink
from lib_bgp_simulator import Relationships, BGPRIBsAS, BGPAS, Relationships, LocalRib, run_example

from bgp_simulator_policies import PAnn, DownOnlyAS, BGPsecAS, BGPsecTransitiveAS, BGPsecTransitiveDownOnlyAS

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
    a = BGPsecAS(1)
    a.recv_q.add_ann(ann1)
    a.process_incoming_anns(a, Relationships.CUSTOMERS)
    # assert announcement was accepted to local rib
    assert(a.local_rib.get_ann(prefix).origin == ann1.origin)
    # Now add announcement with valid signatures
    a.recv_q.add_ann(ann2)
    a.process_incoming_anns(a, Relationships.CUSTOMERS)
    # assert new announcement was accepted to local rib
    assert(a.local_rib.get_ann(prefix).origin == ann2.origin)

@pytest.mark.parametrize("BasePolicyCls", [BGPsecAS, BGPsecTransitiveAS, BGPsecTransitiveDownOnlyAS])
def test_bgpsec_update_attrs(BasePolicyCls):
    """Test updating of bgpsec attributes when forwarding a bgpsec ann"""
    prefix = '137.99.0.0/16'
    ann = PAnn(prefix=prefix, as_path=(13796,),timestamp=0, recv_relationship=Relationships.ORIGIN)
    ann.bgpsec_path = ann.as_path
    ann.next_as = 1
    a.customers = [b]
    a = BasePolicyCls(1)
    b = BasePolicyCls(2)
    a.recv_q.add_ann(ann)
    a.process_incoming_anns(a, Relationships.CUSTOMERS)
    a._populate_send_q(a, Relationships.CUSTOMERS, [Relationships.CUSTOMERS])
    assert(a.send_q.get_send_info(b, prefix).ann.bgpsec_path == (1, 13796) and 
           a.send_q.get_send_info(b, prefix).ann.next_as == 2)

def test_bgpsec_remove_attrs():
    """Test removal of bgpsec attributes when a non-adopting AS is detected on the path"""
    prefix = '137.99.0.0/16'
    ann = PAnn(prefix=prefix, as_path=(13795, 13796),timestamp=0, recv_relationship=Relationships.ORIGIN)
    ann.bgpsec_path = (13796)
    ann.next_as = 13795
    a.customers = [b]
    a = BGPsecAS(1)
    b = BGPsecAS(2)
    a.recv_q.add_ann(ann)
    a.process_incoming_anns(a, Relationships.CUSTOMERS)
    a._populate_send_q(a, Relationships.CUSTOMERS, [Relationships.CUSTOMERS])
    assert(len(a.send_q.get_send_info(b, prefix).ann.bgpsec_path) == 0 and 
           a.send_q.get_send_info(b, prefix).ann.next_as == 0)

@pytest.mark.parametrize("BasePolicyCls", [BGPsecAS, BGPsecTransitiveAS, BGPsecTransitiveDownOnlyAS])
def test_propagate_bgpsec(BasePolicyCls):
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
    as_policies[2] = BGPRIBsAS

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
        1: {prefix: PAnn(as_path=(1, 3, 4, 5), bgpsec_path=(1, 3, 4, 5), next_as=1, recv_relationship=Relationships.CUSTOMERS, **kwargs)},
        2: {prefix: PAnn(as_path=(2, 5), bgpsec_path=(5,), next_as=5, recv_relationship=Relationships.CUSTOMERS, **kwargs)},
        3: {prefix: PAnn(as_path=(3, 4, 5), bgpsec_path=(3, 4, 5), next_as=3, recv_relationship=Relationships.CUSTOMERS, **kwargs)},
        4: {prefix: PAnn(as_path=(4, 5), bgpsec_path=(4, 5), next_as=4, recv_relationship=Relationships.CUSTOMERS, **kwargs)},
        5: {prefix: announcements[0]},
    }

    run_example(peers=peers,
                customer_providers=customer_providers,
                as_policies=as_policies,
                announcements=announcements,
                local_ribs=local_ribs)
