import pytest

from lib_bgp_simulator import Relationships, BGPRIBSPolicy, BGPAS

from bgp_simulator_policies import PAnn, DownOnlyPolicy, BGPsecPolicy, BGPsecTransitivePolicy

@pytest.mark.parametrize("partial, full", [[(1, 3), (1, 2, 3)],
                                           [(1,), (1, 2, 3)],
                                           [(1, 4, 5), (1, 2, 3, 4, 5)],
                                           [(1, 2, 3), (1, 2, 3)]])
def test_partial_path(partial, full):
    a = BGPAS(1) 
    a.policy = BGPsecTransitivePolicy()
    assert(a.policy._partial_verify_path(partial, full))

@pytest.mark.parametrize("partial, full", [[(4,), (1, 2, 3)],
                                           [(5, 4), (1, 2, 3, 4, 5)]])
def test_partial_path(partial, full):
    a = BGPAS(1) 
    a.policy = BGPsecTransitivePolicy()
    assert(not a.policy._partial_verify_path(partial, full))


@pytest.mark.parametrize("partial, full, segments", [[(1, 3), (1, 2, 3), 1],
                                           [(1,), (1, 2, 3), 1],
                                           [(1, 4, 5), (1, 2, 3, 4, 5), 1],
                                           [(1, 2, 3), (1, 2, 3), 0]])
def test_partial_path_metric(partial, full, segments):
    a = BGPAS(1) 
    a.policy = BGPsecTransitivePolicy()
    assert(a.policy._partial_path_metric(partial, full) == segments)
