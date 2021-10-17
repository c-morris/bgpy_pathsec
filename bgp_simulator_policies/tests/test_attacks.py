import pytest

from lib_bgp_simulator import Relationships, BGPRIBSPolicy, BGPAS

from bgp_simulator_policies import PAnn, IntentionalLeak

@pytest.mark.parametrize("bgpsec_path, as_path, result",
    [[(2,), (2,), (2,)],
    [(2, 3), (2, 3), (2, 3)],
    [(2, 4), (2, 3, 4), (2, 3, 4)],
    [(4,), (2, 3, 4), (3, 4)],
])
def test_truncate_path(bgpsec_path, as_path, result):
    a = IntentionalLeak()
    ann = PAnn(prefix="137.99.0.0/16",
               timestamp=0,
               as_path=as_path,
               bgpsec_path=bgpsec_path,
               next_as=1,
               recv_relationship=Relationships.PROVIDERS)
    a._truncate_ann(ann)
    assert(ann.as_path == result)