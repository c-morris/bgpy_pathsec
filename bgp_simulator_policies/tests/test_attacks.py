import pytest

from lib_bgp_simulator import Relationships

from bgp_simulator_policies import PTestAnn, IntentionalLeak, AccidentalLeak, NeighborHijack, OriginHijack, IntentionalLeakNoHash

@pytest.mark.parametrize("bgpsec_path, as_path, result",
    [[(2,), (0, 2,), (2,)],
    [(2, 3), (0, 2, 3), (2, 3)],
    [(2, 4), (0, 2, 3, 4), (2, 3, 4)],
    [(2, 3, 4, 5), (0, 2, 3, 4, 5), (2, 3, 4, 5)],
    [(4,), (0, 2, 3, 4), (3, 4)],
])
def test_truncate_path_hash(bgpsec_path, as_path, result):
    ann = PTestAnn(prefix="137.99.0.0/16",
               timestamp=0,
               as_path=as_path,
               bgpsec_path=bgpsec_path,
               next_as=1,
               recv_relationship=Relationships.PROVIDERS)
    IntentionalLeak._truncate_ann(ann)
    assert(ann.as_path == result)

@pytest.mark.parametrize("bgpsec_path, as_path, result",
    [[(2,), (2,), (2,)],
    [(2, 3), (2, 3), (2, 3)],
    [(2, 4), (2, 3, 4), (3, 4)],
    [(4,), (2, 3, 4), (3, 4)],
])
def test_truncate_path_nohash(bgpsec_path, as_path, result):
    ann = PTestAnn(prefix="137.99.0.0/16",
               timestamp=0,
               as_path=as_path,
               bgpsec_path=bgpsec_path,
               next_as=1,
               recv_relationship=Relationships.PROVIDERS)
    IntentionalLeakNoHash._truncate_ann(ann)
    assert(ann.as_path == result)
