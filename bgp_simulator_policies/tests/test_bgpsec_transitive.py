import pytest

from lib_bgp_simulator import Relationships, BGPRIBSPolicy, BGPAS

from bgp_simulator_policies import PAnn, DownOnlyPolicy, BGPsecPolicy, BGPsecTransitivePolicy

# In BGPsec, an attacker should never send an invalid signature. It is always
# more advantageous to strip the security attributes and send a legacy
# announcement, which will likely be depreferred, but should not be rejected
# outright. 

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
