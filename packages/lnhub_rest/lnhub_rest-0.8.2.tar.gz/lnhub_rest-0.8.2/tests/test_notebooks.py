import os
from pathlib import Path

from nbproject._logger import logger
from nbproject.dev import test


def test_notebooks():
    # assuming this is in the tests folder
    docs_folder = Path(__file__).parents[1] / "docs/"

    if os.environ["LAMIN_ENV"] == "local":
        logger.debug("\nmigrate")
        test.execute_notebooks(docs_folder, write=True)

    logger.debug("\nchecks")
    test.execute_notebooks(docs_folder / "01-checks/", write=True)

    logger.debug("\naccount")
    test.execute_notebooks(docs_folder / "02-account/", write=True)

    logger.debug("\ninstance")
    test.execute_notebooks(docs_folder / "03-instance/", write=True)

    logger.debug("\nstorage")
    test.execute_notebooks(docs_folder / "04-storage/", write=True)

    logger.debug("\norganization")
    test.execute_notebooks(docs_folder / "05-organization/", write=True)
