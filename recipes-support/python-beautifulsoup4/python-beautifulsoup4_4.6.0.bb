DESCRIPTION = "Screen-scraping library"
HOMEPAGE = "https://pypi.python.org/pypi/beautifulsoup4/"
SECTION = "devel/python"
LICENSE = "Apache-2.0"
LIC_FILES_CHKSUM = "file://COPYING.txt;md5=f2d38d8a40bf73fd4b3d16ca2e5882d1"

PR = "r0"
SRCNAME = "beautifulsoup4"

SRC_URI = "https://pypi.python.org/packages/fa/8d/1d14391fdaed5abada4e0f63543fef49b8331a34ca60c88bd521bcf7f782/${SRCNAME}-${PV}.tar.gz"

SRC_URI[md5sum] = "c17714d0f91a23b708a592cb3c697728"

S = "${WORKDIR}/${SRCNAME}-${PV}"

inherit setuptools

# avoid "error: option --single-version-externally-managed not recognized"
DISTUTILS_INSTALL_ARGS = "--root=${D} \
    --prefix=${prefix} \
    --install-lib=${PYTHON_SITEPACKAGES_DIR} \
    --install-data=${datadir}"

