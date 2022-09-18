import pytest

from bgp_simulator_pkg import Relationships

from bgp_simulator_policies import PTestAnn, BGPsecAS
from bgp_simulator_policies import BGPsecTransitiveAS
from bgp_simulator_policies import BGPsecTransitiveDownOnlyAS


# In BGPsec, an attacker should never send an invalid signature. It is always
# more advantageous to strip the security attributes and send a legacy
# announcement, which will likely be depreferred, but should not be rejected
# outright.


def test_process_incoming_anns_bgpsec_depref():
    """Test preference of ann from customer with a BGPsec signature"""
    prefix = '137.99.0.0/16'
    ann1 = PTestAnn(prefix=prefix, as_path=(2, 13796), timestamp=0,
                    recv_relationship=Relationships.ORIGIN)
    ann2 = PTestAnn(prefix=prefix, as_path=(13795,), timestamp=0,
                    recv_relationship=Relationships.ORIGIN)
    ann2.bgpsec_path = ann2.as_path
    ann2.next_as = 1
    a = BGPsecAS(1)
    # Remove these later when they're fixed
    a.providers = tuple()
    a.peers = tuple()
    a.customers = tuple()
    a._recv_q.add_ann(ann1)
    a.process_incoming_anns(from_rel=Relationships.CUSTOMERS,
                            propagation_round=0,
                            scenario=None)
    # assert announcement was accepted to local rib
    assert (a._local_rib.get_ann(prefix).origin == ann1.origin)
    # Now add announcement with valid signatures
    a._recv_q.add_ann(ann2)
    a.process_incoming_anns(from_rel=Relationships.CUSTOMERS,
                            propagation_round=0,
                            scenario=None)
    # assert new announcement was accepted to local rib
    assert (a._local_rib.get_ann(prefix).origin == ann2.origin)


pols = [BGPsecAS, BGPsecTransitiveAS, BGPsecTransitiveDownOnlyAS]


@pytest.mark.parametrize("BasePolicyCls", pols)
def test_bgpsec_update_attrs(BasePolicyCls):
    """Test updating of bgpsec attributes when forwarding a bgpsec ann"""
    prefix = '137.99.0.0/16'
    ann = PTestAnn(prefix=prefix, as_path=(13796,), timestamp=0,
                   recv_relationship=Relationships.ORIGIN)
    ann.bgpsec_path = ann.as_path
    ann.next_as = 1
    a = BasePolicyCls(1)
    b = BasePolicyCls(2)
    # Remove these later when they're fixed
    a.providers = tuple()
    a.peers = tuple()
    a.customers = tuple()
    a.customers = [b]
    a._recv_q.add_ann(ann)
    a.process_incoming_anns(from_rel=Relationships.CUSTOMERS,
                            propagation_round=0,
                            scenario=None)
    a._populate_send_q(Relationships.CUSTOMERS, [Relationships.CUSTOMERS])
    assert (a._send_q.get_send_info(b, prefix).ann.bgpsec_path == (1, 13796) and # noqa E501
            a._send_q.get_send_info(b, prefix).ann.next_as == 2)


def test_bgpsec_remove_attrs():
    """Test removal of bgpsec attributes when a non-adopting AS is detected on
    the path"""
    prefix = '137.99.0.0/16'
    ann = PTestAnn(prefix=prefix, as_path=(13795, 13796), timestamp=0,
                   recv_relationship=Relationships.ORIGIN)
    ann.bgpsec_path = (13796,)
    ann.next_as = 13795
    a = BGPsecAS(1)
    b = BGPsecAS(2)
    # Remove these later when they're fixed
    a.providers = tuple()
    a.peers = tuple()
    a.customers = tuple()
    a.customers = [b]
    a._recv_q.add_ann(ann)
    a.process_incoming_anns(from_rel=Relationships.CUSTOMERS,
                            propagation_round=0,
                            scenario=None)
    a._populate_send_q(Relationships.CUSTOMERS, [Relationships.CUSTOMERS])
    assert (len(a._send_q.get_send_info(b, prefix).ann.bgpsec_path) == 0 and
           a._send_q.get_send_info(b, prefix).ann.next_as == 0)
