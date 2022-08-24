from pathlib import Path
import pytest

from bgp_simulator_pkg import EngineTester
from bgp_simulator_pkg import EngineTestConfig


from .engine_test_configs import Config001
from .engine_test_configs import Config002
from .engine_test_configs import Config003
from .engine_test_configs import Config004
from .engine_test_configs import Config005
from .engine_test_configs import Config006
from .engine_test_configs import Config007
from .engine_test_configs import Config008
from .engine_test_configs import Config009
from .engine_test_configs import Config010
from .engine_test_configs import Config011
from .engine_test_configs import Config012
from .engine_test_configs import Config013
from .engine_test_configs import Config014
from .engine_test_configs import Config015
from .engine_test_configs import Config016
from .engine_test_configs import Config017
from .engine_test_configs import Config018
from .engine_test_configs import Config019


@pytest.mark.engine
class TestEngine:
    """Performs a system test on the engine

    See README for in depth details
    """

    @pytest.mark.parametrize("conf",
                             [Config001,
                              Config002,
                              Config003,
                              Config004,
                              Config005,
                              Config006,
                              Config007,
                              Config008,
                              Config009,
                              Config010,
                              Config011,
                              Config012,
                              Config013,
                              Config014,
                              Config015,
                              Config016,
                              Config017,
                              Config018,
                              Config019,
                              ])
    def test_engine(self, conf: EngineTestConfig, overwrite: bool):
        """Performs a system test on the engine

        See README for in depth details
        """

        EngineTester(base_dir=self.base_dir,
                     conf=conf,
                     overwrite=overwrite).test_engine()

    @property
    def base_dir(self) -> Path:
        """Returns test output dir"""

        return Path(__file__).parent / "engine_test_outputs"
