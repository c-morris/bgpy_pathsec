import pytest

from bgpy import Relationships

from bgpy_pathsec import PathManipulationAnn
from bgpy_pathsec import BGPsecTransitiveAS


t1 = [
    [(1, 3), (1, 2, 3), 1],
    [(1,), (1, 2, 3), 1],
    [(777,), (2, 777), 1],
    [(4, 5), (2, 3, 4, 5), 1],
    [(1, 4, 5), (1, 2, 3, 4, 5), 1],
    [(2, 3), (2, 3), 0],
    [(1, 2, 3), (1, 2, 3), 0],
]


@pytest.mark.parametrize("partial, full, segments", t1)
def test_partial_path_metric(partial, full, segments):
    a = BGPsecTransitiveAS(1)
    assert a._partial_path_metric(partial, full) == segments


def test_process_incoming_anns_bgpsec_transitive_reject():
    """Test rejection of bgpsec transitive ann with missing signature"""
    prefix = "137.99.0.0/16"
    ann = PathManipulationAnn(
        prefix=prefix,
        as_path=(13795,),
        timestamp=0,
        recv_relationship=Relationships.ORIGIN,
        seed_asn=None,
        roa_valid_length=None,
        roa_origin=None,
        bgpsec_path=tuple(),
        next_as=1,
        removed_signatures=(13795,),
    )
    a = BGPsecTransitiveAS(1)
    # Now add announcement with missing signatures
    a._recv_q.add_ann(ann)
    a.process_incoming_anns(
        from_rel=Relationships.CUSTOMERS, propagation_round=0, scenario=None
    )
    # assert new announcement was not accepted to local rib
    assert a._local_rib.get_ann(prefix) is None
