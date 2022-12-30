import pytest

from bgp_simulator_pkg import Relationships

from bgp_simulator_pathsec_policies import PathManipulationAnn, DownOnlyAS, BGPsecAS
from bgp_simulator_pathsec_policies import BGPsecTransitiveAS
from bgp_simulator_pathsec_policies import BGPsecTransitiveDownOnlyAS


pols = [DownOnlyAS, BGPsecAS, BGPsecTransitiveAS, BGPsecTransitiveDownOnlyAS]


@pytest.mark.parametrize("AdoptedPolicy", pols)
def test_process_incoming_anns_do(AdoptedPolicy):
    """Test basic functionality of process_incoming_anns"""
    prefix = '137.99.0.0/16'
    ann = PathManipulationAnn(prefix=prefix, as_path=(13796,), timestamp=0,
                   recv_relationship=Relationships.ORIGIN, seed_asn=None,
                   roa_valid_length=None, roa_origin=None)
    a = AdoptedPolicy(1)
    a._recv_q.add_ann(ann)
    a.process_incoming_anns(from_rel=Relationships.CUSTOMERS,
                            propagation_round=0,
                            scenario=None)
    # assert announcement was accepted to local rib
    assert (a._local_rib.get_ann(prefix).origin == ann.origin)