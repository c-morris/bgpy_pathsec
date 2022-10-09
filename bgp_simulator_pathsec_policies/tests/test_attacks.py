import pytest

from bgp_simulator_pkg import Relationships

from bgp_simulator_pathsec_policies import PTestAnn, IntentionalLeak
from bgp_simulator_pathsec_policies import IntentionalLeakNoHash, TwoHopAttack

t1 = ([[(2,), (0, 2,), (2,)],
       [(2, 3), (0, 2, 3), (2, 3)],
       [(5,), (0, 2, 3, 4, 5), (4, 5)],
       [(1239, 17676, 23831), (138088, 4800, 1239, 17676, 23831), (4800, 1239, 17676, 23831)], # noqa E501
       [(21263, 44398), (209044, 21263, 3356, 3292, 44398), (3356, 3292, 44398)], # noqa E501
       [(174, 6461, 29829), (202617, 174, 6461, 29829), (174, 6461, 29829)],
       [(2, 4), (0, 2, 3, 4), (3, 4)],
       [(2, 3, 4, 5), (0, 2, 3, 1, 4, 5), (2, 3, 1, 4, 5)],
       [(1, 2, 3, 4, 5), (0, 1, 2, 3, 4, 5), (1, 2, 3, 4, 5)],
       [(2, 3, 4, 5), (0, 2, 3, 4, 5), (2, 3, 4, 5)],
       [(4,), (0, 2, 3, 4), (3, 4)],
      ]) # noqa E124


@pytest.mark.parametrize("bgpsec_path, as_path, result", t1)
def test_truncate_path_hash(bgpsec_path, as_path, result):
    ann = PTestAnn(prefix="137.99.0.0/16",
                   timestamp=0,
                   as_path=as_path,
                   bgpsec_path=bgpsec_path,
                   next_as=1,
                   recv_relationship=Relationships.PROVIDERS)
    IntentionalLeak._truncate_ann(None, ann)
    assert (ann.as_path == result)


t2 = ([[(2,), (0, 2,), (2,)],
       [(2, 3), (0, 2, 3), (2, 3)],
       [(2, 4), (0, 2, 3, 4), (3, 4)],
       [(2, 3, 4, 5), (0, 2, 3, 1, 4, 5), (1, 4, 5)],
       [(1239, 17676, 23831), (138088, 4800, 1239, 17676, 23831), (4800, 1239, 17676, 23831)], # noqa E501
       [(2, 3, 5), (0, 2, 3, 1, 4, 5), (4, 5)],
       [(5,), (0, 2, 3, 4, 5), (4, 5)],
       [(1, 2, 3, 4, 5), (0, 1, 2, 3, 4, 5), (1, 2, 3, 4, 5)],
       [(4,), (0, 2, 3, 4), (3, 4)],
      ]) # noqa E124


@pytest.mark.parametrize("bgpsec_path, as_path, result", t2)
def test_truncate_path_nohash(bgpsec_path, as_path, result):
    ann = PTestAnn(prefix="137.99.0.0/16",
                   timestamp=0,
                   as_path=as_path,
                   bgpsec_path=bgpsec_path,
                   next_as=1,
                   recv_relationship=Relationships.PROVIDERS)
    IntentionalLeakNoHash._truncate_ann(None, ann)
    assert (ann.as_path == result)


t3 = ([[(1, 2, 3), (2, 3)],
       [(4, 1, 2, 3), (2, 3)]])


@pytest.mark.parametrize("as_path, result", t3)
def test_truncate_path_twohop(as_path, result):
    ann = PTestAnn(prefix="137.99.0.0/16",
                   timestamp=0,
                   as_path=as_path,
                   bgpsec_path=(3,),
                   next_as=1,
                   recv_relationship=Relationships.PROVIDERS)
    TwoHopAttack._truncate_ann(None, ann)
    assert (ann.as_path == result)
