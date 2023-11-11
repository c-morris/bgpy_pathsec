from pathlib import Path
import pytest

from bgpy import EngineTester
from bgpy import EngineTestConfig

from .engine_test_configs import *


@pytest.mark.engine
class TestEngine:
    """Performs a system test on the engine

    See README for in depth details
    """

    @pytest.mark.parametrize(
        "conf",
        [
            config_p_001,
            config_p_002,
            config_p_003,
            config_p_004,
            config_p_005,
            config_p_006,
            config_p_007,
            config_p_008,
            config_p_009,
            config_p_010,
            config_p_011,
            config_p_012,
            config_p_013,
            config_p_014,
            #   config_p_015,
            #   config_p_016,
            config_p_017,
            config_p_018,
            config_p_019,
            config_p_020,
            config_p_021,
            config_p_022,
            config_p_024,
            config_p_025,
            config_p_026,
            config_p_027,
            config_p_028,
            config_p_029,
            config_p_030,
            config_p_031,
            config_p_032,
            config_p_033,
            config_p_034,
            config_p_035,
            config_p_036,
            config_p_037,
            config_p_038,
            config_p_039,
            config_p_040,
            config_p_041,
            config_p_042,
            config_p_043,
        ],
    )
    def test_engine(self, conf: EngineTestConfig, overwrite: bool):
        """Performs a system test on the engine

        See README for in depth details
        """

        EngineTester(
            base_dir=self.base_dir, conf=conf, overwrite=overwrite
        ).test_engine()

    @property
    def base_dir(self) -> Path:
        """Returns test output dir"""

        return Path(__file__).parent / "engine_test_outputs"
