import pytest

from lib_caida_collector import PeerLink, CustomerProviderLink as CPLink
from lib_bgp_simulator import Relationships, BGPAS, Relationships, LocalRIB

from bgp_simulator_policies import PTestAnn, DownOnlyAS, BGPsecAS, BGPsecTransitiveAS, BGPsecTransitiveDownOnlyAS

@pytest.mark.parametrize("partial, full", [[(1, 3), (1, 2, 3)],
                                           [(1,), (1, 2, 3)],
                                           [(1, 4, 5), (1, 2, 3, 4, 5)],
                                           [(1, 2, 3), (1, 2, 3)]])
def test_partial_path(partial, full):
    a = BGPsecTransitiveAS(1)
    assert(a._partial_verify_path(partial, full))

@pytest.mark.parametrize("partial, full", [[(4,), (1, 2, 3)],
                                           [(5, 4), (1, 2, 3, 4, 5)]])
def test_partial_path(partial, full):
    a = BGPsecTransitiveAS(1)
    assert(not a._partial_verify_path(partial, full))


@pytest.mark.parametrize("partial, full, segments", [[(1, 3), (1, 2, 3), 1],
                                           [(1,), (1, 2, 3), 1],
                                           [(777,), (2, 777), 1],
                                           [(1, 4, 5), (1, 2, 3, 4, 5), 1],
                                           [(1, 2, 3), (1, 2, 3), 0]])
def test_partial_path_metric(partial, full, segments):
    a = BGPsecTransitiveAS(1)
    assert(a._partial_path_metric(partial, full) == segments)

def test_process_incoming_anns_bgpsec_transitive_reject():
    """Test rejection of bgpsec transitive ann with missing signature"""
    prefix = '137.99.0.0/16'
    ann = PTestAnn(prefix=prefix, as_path=(13795,),timestamp=0, recv_relationship=Relationships.ORIGIN)
    ann.bgpsec_path = tuple()
    ann.next_as = 1
    ann.removed_signatures = (13795,)
    a = BGPsecTransitiveAS(1)
    # Now add announcement with missing signatures
    a._recv_q.add_ann(ann)
    a.process_incoming_anns(Relationships.CUSTOMERS)
    # assert new announcement was not accepted to local rib
    assert(a._local_rib.get_ann(prefix) is None)

