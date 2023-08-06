import logging
from pathlib import Path

import pytest

from dls_utilpack.visit import get_xchem_directory, get_xchem_subdirectory

# Base class for the tester.
from tests.base_tester import BaseTester

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class TestVisit(BaseTester):
    def test(self, constants, logging_setup, output_directory):
        """ """

        self.main(constants, output_directory)

    # ----------------------------------------------------------------------------------------
    async def _main_coroutine(
        self,
        constants,
        output_directory,
    ):
        """ """

        # Check valid visits.
        assert get_xchem_subdirectory("aa12345-1") == "aa12345/aa12345-1"
        assert get_xchem_subdirectory("aa12345-1234") == "aa12345/aa12345-1234"
        assert get_xchem_subdirectory("aa12345-1234_") == "aa12345/aa12345-1234"
        assert (
            get_xchem_subdirectory("aa12345-1234_some stuff") == "aa12345/aa12345-1234"
        )

        # Check invalid visit formats.
        with pytest.raises(ValueError) as excinfo:
            get_xchem_subdirectory("aa12345")
        assert "convention" in str(excinfo.value)

        with pytest.raises(ValueError) as excinfo:
            get_xchem_subdirectory("a12345-1")
        assert "convention" in str(excinfo.value)

        with pytest.raises(ValueError) as excinfo:
            get_xchem_subdirectory("[aa12345-1]")
        assert "convention" in str(excinfo.value)

        with pytest.raises(ValueError) as excinfo:
            get_xchem_subdirectory("aa12345-1-somestuff")
        assert "convention" in str(excinfo.value)

        # Check good directory.
        parent = Path(output_directory) / "processing/lab36"
        full_path = parent / "aa12345/aa12345-1"
        full_path.mkdir(parents=True, exist_ok=True)

        assert get_xchem_directory(str(parent), "aa12345-1") == str(full_path)

        # Check invalid directory.
        with pytest.raises(RuntimeError) as excinfo:
            get_xchem_directory("something", "aa12345-1")
        assert "does not exist" in str(excinfo.value)
