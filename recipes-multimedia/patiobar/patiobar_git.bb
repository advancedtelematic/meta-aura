SUMMARY = "A web frontend for pianobar, which is a CLI frontend for Pandora."

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=220c032936694298a846ea64b78d2cb7"

SRC_URI = "git://github.com/tkfu/Patiobar.git;protocol=https \
           file://patiobar.service \
           file://start-patiobar.py \
           "

RDEPENDS_${PN} += " bash pianobar python-beautifulsoup4 screen nodejs"

PV = "1.0.0+git${SRCPV}"
SRCREV = "f0421a62233f978202ccf531970350cfcf4d99a3"
NPM_INSTALLDIR = "${D}${libdir}/node_modules/${PN}"
FILES_${PN} += " \
    ${libdir}/node_modules/${PN} \
    /etc/patiobar.env \
    /usr/bin/start-patiobar.py \
    ${@bb.utils.contains('DISTRO_FEATURES', 'systemd', '${systemd_unitdir}/system/patiobar.service', '', d)} \
"

inherit npm-install systemd

# Must be set after inherit npm since that itself sets S
S = "${WORKDIR}/git"
LICENSE_${PN} = "MIT"

export PANDORA_USER
export PANDORA_PASSWORD
export PANDORA_PROXY

do_install() {
	install -d ${NPM_INSTALLDIR}/
	cp -a ${S}/* ${NPM_INSTALLDIR}/ --no-preserve=ownership
	echo "PIANOBAR_FIFO=/home/root/.config/pianobar/ctl" > ${WORKDIR}/patiobar.env
	echo "PANDORA_USER=${PANDORA_USER}" >> ${WORKDIR}/patiobar.env
	echo "PANDORA_PASSWORD=${PANDORA_PASSWORD}" >> ${WORKDIR}/patiobar.env
	echo "PATIOBAR_DIR=${libdir}/node_modules/${PN}" >> ${WORKDIR}/patiobar.env
	echo "PIANOBAR_PROXY=${PANDORA_PROXY}" >> ${WORKDIR}/patiobar.env
	echo "HOME=/home/root" >> ${WORKDIR}/patiobar.env
	install -d ${D}/etc
	install -d ${D}/usr/bin
	install -m 0644 ${WORKDIR}/patiobar.env ${D}/etc/patiobar.env
	install -m 0755 ${WORKDIR}/start-patiobar.py ${D}/usr/bin/start-patiobar.py
	if ${@bb.utils.contains('DISTRO_FEATURES', 'systemd', 'true', 'false', d)}; then
      install -d ${D}/${systemd_unitdir}/system
      install -m 0644 ${WORKDIR}/patiobar.service ${D}/${systemd_unitdir}/system/patiobar.service
    fi
	
}

