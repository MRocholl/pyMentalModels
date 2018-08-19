from os.path import realpath, dirname, join as path_join
from setuptools import setup, find_packages

NAME = "pyMentalModels"
DESCRIPTION = "Python implementation of the msentential reasoner"
LONG_DESCRIPTION = open("README.rst").read()
MAINTAINER = "Moritz Rocholl"
MAINTAINER_EMAIL = "moritz.rocholl@gmail.com"
URL = "https://gkigit.informatik.uni-freiburg.de/coco/mentalmodels.git"
license = "MIT"
VERSION = "0.0.9"

PROJECT_ROOT = dirname(realpath(__file__))
REQUIREMENTS_FILE = path_join(PROJECT_ROOT, "requirements.txt")

with open(REQUIREMENTS_FILE, "r") as f:
    INSTALL_REQUIREMENTS = f.read().splitlines()

SETUP_REQUIREMENTS = ["pytest-runner"]
TEST_REQUIREMENTS = ["pytest", "pytest-cov"]


if __name__ == "__main__":
    setup(
        name=NAME,
        version=VERSION,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        url=URL,
        scripts=["scripts/mmreasoner"],
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        package_data={"docs": ["*"]},
        include_package_data=True,
        install_requires=INSTALL_REQUIREMENTS,
        setup_requires=SETUP_REQUIREMENTS,
        tests_require=TEST_REQUIREMENTS,
    )
