import pytest

from bgp_simulator_pkg import Relationships

from bgp_simulator_policies import PTestAnn, DownOnlyAS


def test_process_incoming_anns_do_reject():
    """Test rejection of ann from customer with DO community"""
    prefix = '137.99.0.0/16'
    ann = PTestAnn(prefix=prefix, as_path=(13796,), timestamp=0,
                   recv_relationship=Relationships.ORIGIN)
    ann.do_communities = (13796,)
    a = DownOnlyAS(1)
    a._recv_q.add_ann(ann)
    a.process_incoming_anns(from_rel=Relationships.CUSTOMERS,
                            propagation_round=0,
                            scenario=None)
    # assert announcement was accepted to local rib
    assert (a._local_rib.get_ann(prefix) is None)


def test_process_incoming_anns_do_accept():
    """Test acceptance of ann from non-customer with DO community"""
    prefix = '137.99.0.0/16'
    ann = PTestAnn(prefix=prefix, as_path=(13796,), timestamp=0,
                   recv_relationship=Relationships.ORIGIN)
    ann.do_communities = (13796,)
    a = DownOnlyAS(1)
    a._recv_q.add_ann(ann)
    a.process_incoming_anns(from_rel=Relationships.PROVIDERS,
                            propagation_round=0,
                            scenario=None)
    # assert announcement was accepted to local rib
    assert (a._local_rib.get_ann(prefix).origin == ann.origin)


@pytest.mark.parametrize("b_relationship, community_len",
                          [[Relationships.CUSTOMERS, 1], # noqa E127
                           [Relationships.PROVIDERS, 0]])
def test_populate_send_q_do(b_relationship, community_len):
    """Test addition of DO community when propagating to customers"""
    prefix = '137.99.0.0/16'
    ann = PTestAnn(prefix=prefix, as_path=(13796,), timestamp=0,
                   recv_relationship=Relationships.ORIGIN)
    a = DownOnlyAS(1)
    b = DownOnlyAS(2)
    setattr(a, b_relationship.name.lower(), (b,))
    a._recv_q.add_ann(ann)
    a.process_incoming_anns(from_rel=Relationships.CUSTOMERS,
                            propagation_round=0,
                            scenario=None)
    a._populate_send_q(b_relationship, [Relationships.CUSTOMERS])
    assert (len(a._send_q.get_send_info(b, prefix).ann.do_communities) ==
           community_len)
