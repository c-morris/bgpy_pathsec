from pathlib import Path
import pytest

from bgp_simulator_pkg import EngineTester
from bgp_simulator_pkg import EngineTestConfig

from .engine_test_configs import *


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
                              Config020,
                              Config021,
                              Config022,
                              Config023,
                              Config024,
                              Config025,
                              Config026,
                              Config027,
                              Config028,
                              Config029,
                              Config030,
                              Config031,
                              Config032,
                              Config033,
                              Config034,
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
