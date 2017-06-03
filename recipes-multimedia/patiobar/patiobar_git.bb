SUMMARY = "A web frontend for pianobar, which is a CLI frontend for Pandora."

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=220c032936694298a846ea64b78d2cb7"

SRC_URI = "git://github.com/tkfu/Patiobar.git;protocol=https \
           npm://registry.npmjs.org;name=express;version=4.6.1;subdir=node_modules/express \
           npm://registry.npmjs.org;name=socket.io;version=1.0.6;subdir=node_modules/socket.io \
           file://get-us-proxy.py \
           "

RDEPENDS_${PN} += "bash pianobar python-beautifulsoup4 screen"

PV = "1.0.0+git${SRCPV}"
SRCREV = "f0421a62233f978202ccf531970350cfcf4d99a3"

NPM_SHRINKWRAP := "${THISDIR}/${PN}/npm-shrinkwrap.json"
NPM_LOCKDOWN := "${THISDIR}/${PN}/lockdown.json"

inherit npm

# Must be set after inherit npm since that itself sets S
S = "${WORKDIR}/git"
LICENSE_${PN} = "MIT"
