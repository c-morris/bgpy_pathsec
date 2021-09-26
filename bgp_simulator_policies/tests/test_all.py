import pytest

from lib_bgp_simulator import Relationships, BGPRIBSPolicy, BGPAS

from bgp_simulator_policies import PAnn, DownOnlyPolicy, BGPsecPolicy

@pytest.mark.parametrize("AdoptedPolicy", [DownOnlyPolicy, BGPsecPolicy])
def test_process_incoming_anns_do(AdoptedPolicy):
    """Test basic functionality of process_incoming_anns"""
    prefix = '137.99.0.0/16'
    ann = PAnn(prefix=prefix, as_path=(13796,),timestamp=0)
    a = BGPAS(1) 
    a.policy = AdoptedPolicy()
    a.policy.recv_q[13796][prefix].append(ann)
    a.policy.process_incoming_anns(a, Relationships.CUSTOMERS)
    # assert announcement was accepted to local rib
    assert(a.policy.local_rib[prefix].origin == ann.origin)


