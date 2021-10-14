import pytest

from lib_caida_collector import PeerLink, CustomerProviderLink as CPLink
from lib_bgp_simulator import Relationships, BGPRIBsAS, BGPAS, Relationships, LocalRib, run_example

from bgp_simulator_policies import PAnn, DownOnlyAS, BGPsecAS, BGPsecTransitiveAS, BGPsecTransitiveDownOnlyAS

@pytest.mark.parametrize("partial, full", [[(1, 3), (1, 2, 3)],
                                           [(1,), (1, 2, 3)],
                                           [(1, 4, 5), (1, 2, 3, 4, 5)],
                                           [(1, 2, 3), (1, 2, 3)]])
def test_partial_path(partial, full):
    a = BGPAS(1) 
    a = BGPsecTransitiveAS()
    assert(a._partial_verify_path(partial, full))

@pytest.mark.parametrize("partial, full", [[(4,), (1, 2, 3)],
                                           [(5, 4), (1, 2, 3, 4, 5)]])
def test_partial_path(partial, full):
    a = BGPAS(1) 
    a = BGPsecTransitiveAS()
    assert(not a._partial_verify_path(partial, full))


@pytest.mark.parametrize("partial, full, segments", [[(1, 3), (1, 2, 3), 1],
                                           [(1,), (1, 2, 3), 1],
                                           [(1, 4, 5), (1, 2, 3, 4, 5), 1],
                                           [(1, 2, 3), (1, 2, 3), 0]])
def test_partial_path_metric(partial, full, segments):
    a = BGPAS(1) 
    a = BGPsecTransitiveAS()
    assert(a._partial_path_metric(partial, full) == segments)

def test_process_incoming_anns_bgpsec_transitive_reject():
    """Test rejection of bgpsec transitive ann with missing signature"""
    prefix = '137.99.0.0/16'
    ann = PAnn(prefix=prefix, as_path=(13795,),timestamp=0, recv_relationship=Relationships.ORIGIN)
    ann.bgpsec_path = tuple()
    ann.next_as = 1
    ann.removed_signatures = (13795,)
    a = BGPAS(1) 
    a = BGPsecTransitiveAS()
    # Now add announcement with missing signatures
    a.recv_q.add_ann(ann)
    a.process_incoming_anns(a, Relationships.CUSTOMERS)
    # assert new announcement was not accepted to local rib
    assert(a.local_rib.get_ann(prefix) is None)

@pytest.mark.parametrize("BaseASCls", [BGPsecTransitiveAS, BGPsecTransitiveDownOnlyAS])
def test_propagate_bgpsec_transitive1(BaseASCls):
    r"""
    Test BGPsec transitive preference for fewer nonadopting segments.
    Horizontal lines are peer relationships, vertical lines are customer-provider. 
                                                                             
      1                                                                         
     / \                                                                         
    2   3                                                                     
    |   |
    6   7
    |   |
    8   9
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
                          CPLink(provider_asn=2, customer_asn=6),
                          CPLink(provider_asn=3, customer_asn=7),
                          CPLink(provider_asn=4, customer_asn=5),
                          CPLink(provider_asn=6, customer_asn=8),
                          CPLink(provider_asn=7, customer_asn=9),
                          CPLink(provider_asn=8, customer_asn=5),
                          CPLink(provider_asn=9, customer_asn=4),
                          ]
    # Number identifying the type of AS class
    as_policies = {asn: BaseASCls for asn in
                   list(range(1, 10))}
    # Multiple short segments
    as_policies[2] = BGPRIBsAS
    as_policies[8] = BGPRIBsAS
    # Long single segment
    as_policies[4] = BGPRIBsAS
    as_policies[9] = BGPRIBsAS
    as_policies[7] = BGPRIBsAS
    as_policies[3] = BGPRIBsAS

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
        1: {prefix: PAnn(as_path=(1, 3, 7, 9, 4, 5), bgpsec_path=(1, 5), next_as=1, recv_relationship=Relationships.CUSTOMERS, **kwargs)},
        2: {prefix: PAnn(as_path=(2, 6, 8, 5), bgpsec_path=(6, 5), next_as=2, recv_relationship=Relationships.CUSTOMERS, **kwargs)},
        3: {prefix: PAnn(as_path=(3, 7, 9, 4, 5), bgpsec_path=(5,), next_as=4, recv_relationship=Relationships.CUSTOMERS, **kwargs)},
        4: {prefix: PAnn(as_path=(4, 5), bgpsec_path=(5,), next_as=4, recv_relationship=Relationships.CUSTOMERS, **kwargs)},
        5: {prefix: announcements[0]},
        6: {prefix: PAnn(as_path=(6, 8, 5), bgpsec_path=(6, 5), next_as=6, recv_relationship=Relationships.CUSTOMERS, **kwargs)},
        7: {prefix: PAnn(as_path=(7, 9, 4, 5), bgpsec_path=(5,), next_as=4, recv_relationship=Relationships.CUSTOMERS, **kwargs)},
        8: {prefix: PAnn(as_path=(8, 5), bgpsec_path=(5,), next_as=8, recv_relationship=Relationships.CUSTOMERS, **kwargs)},
        9: {prefix: PAnn(as_path=(9, 4, 5), bgpsec_path=(5,), next_as=4, recv_relationship=Relationships.CUSTOMERS, **kwargs)},
    }

    run_example(peers=peers,
                customer_providers=customer_providers,
                as_policies=as_policies,
                announcements=announcements,
                local_ribs=local_ribs)
