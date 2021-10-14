import pytest

from lib_bgp_simulator import Relationships, BGPRIBsAS, BGPAS

from bgp_simulator_policies import PAnn, DownOnlyAS, BGPsecAS, BGPsecTransitiveAS, BGPsecTransitiveDownOnlyAS

@pytest.mark.parametrize("AdoptedPolicy", [DownOnlyAS, BGPsecAS, BGPsecTransitiveAS, BGPsecTransitiveDownOnlyAS])
def test_process_incoming_anns_do(AdoptedPolicy):
    """Test basic functionality of process_incoming_anns"""
    prefix = '137.99.0.0/16'
    ann = PAnn(prefix=prefix, as_path=(13796,),timestamp=0, recv_relationship=Relationships.ORIGIN)
    a = AdoptedPolicy(1)
    a.recv_q.add_ann(ann)
    a.process_incoming_anns(a, Relationships.CUSTOMERS)
    # assert announcement was accepted to local rib
    assert(a.local_rib.get_ann(prefix).origin == ann.origin)
