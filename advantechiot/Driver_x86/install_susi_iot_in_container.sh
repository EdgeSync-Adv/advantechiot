THIS=${0%/*}

LIBE_NAME="libEApi"
LIB3_NAME="libSUSI-3.02"
LIB4_NAME="libSUSI-4.00"
JNI4_NAME="libJNISUSI-4.00"
DEVICE_NAME="libSUSIDevice"
AI_NAME="libSUSIAI"
JANSSON_NAME="libjansson"
IOT_NAME="libSusiIoT"

LINUX_LIB_DIR="/usr/lib"
LINUX_ADV_DIR="/usr/lib/Advantech"
LINUX_SUSI_INI_DIR=${LINUX_ADV_DIR}"/Susi/ini"
LINUX_SUSIIOT_MODULE_DIR=${LINUX_ADV_DIR}"/iot/modules"
CPU_NAME=$(cat /proc/cpuinfo | grep "model name" | uniq)
usage()
{
	cat >&2 <<-eof
	Usage: $0 [u]
	  (Null) : install SUSI 5.0
	  u      : uninstall SUSI 5.0
	  s      : silent install	
	eof
}

install_ai_service()
{
	argument="FFF"
	echo "111111111111"
	if [ "${THIS}" = "." ]; then
		argument=${PWD}/AI/service
	else
		argument=${PWD}/${THIS}/AI/service
	fi
	echo $PWD
	echo $argument
	echo $THIS
	echo "2222222222222"
	target_ai_install_file=${THIS}/AI/service/install_SusiService_in_container.sh
	"$target_ai_install_file" "$argument"
	echo "3333333"
}

remove_ai_service()
{
	target_ai_remove_file=${THIS}/AI/service/unInstall_SusiService_in_container.sh
	"$target_ai_remove_file"
}

installlibrary()
{
	mkdir -p ${LINUX_SUSI_INI_DIR}/
	cp -af ${THIS}/ini/*.ini ${LINUX_SUSI_INI_DIR}/
	cp -a ${THIS}/lib*.* ${LINUX_LIB_DIR}/

	mkdir -p ${LINUX_SUSIIOT_MODULE_DIR}
	cp -af ${THIS}/modules/libSUSIDrv.so ${LINUX_SUSIIOT_MODULE_DIR}/
	cp -af ${THIS}/modules/libDiskInfo.so ${LINUX_SUSIIOT_MODULE_DIR}/
	cp -af ${THIS}/modules/libSUSIDevice.so ${LINUX_SUSIIOT_MODULE_DIR}/
	if echo "${CPU_NAME}" | grep -q "Intel";then
		cp -af ${THIS}/modules/libSUSIAIIoT.so ${LINUX_SUSIIOT_MODULE_DIR}/
	fi
	ldconfig
}

uninstalllibrary()
{
	rm -f ${LINUX_LIB_DIR}/${LIB4_NAME}.*
	rm -f ${LINUX_LIB_DIR}/${LIB3_NAME}.*
	rm -f ${LINUX_LIB_DIR}/${LIBE_NAME}.*
	rm -f ${LINUX_LIB_DIR}/${JNI4_NAME}.*
	rm -f ${LINUX_LIB_DIR}/${DEVICE_NAME}.*
	rm -f ${LINUX_LIB_DIR}/${AI_NAME}.*
	rm -f ${LINUX_LIB_DIR}/${JANSSON_NAME}.*
	rm -f ${LINUX_LIB_DIR}/${IOT_NAME}.*
	ldconfig
	
	rm -rf ${LINUX_ADV_DIR}
}

case ${1} in
	"")
		uninstalllibrary
		remove_ai_service
		if echo "${CPU_NAME}" | grep -q "Intel";then
			echo "Install SUSI AI service."
			install_ai_service
		fi
		echo "Install SUSI library."
		echo "AAAAAAAAA"
		installlibrary
		echo "BBBBBBBB"
		ldconfig -p | grep "${LIB4_NAME}\|${LIB3_NAME}\|${LIBE_NAME}\|${JNI4_NAME}\|${DEVICE_NAME}\|${JANSSON_NAME}\|${IOT_NAME}\|${AI_NAME}"
		;;
	"s")
		uninstalllibrary
		remove_ai_service
		if echo "${CPU_NAME}" | grep -q "Intel";then
			echo "Install SUSI AI service."
			install_ai_service
		fi
		echo "Install SUSI library."
		installlibrary
		ldconfig -p | grep "${LIB4_NAME}\|${LIB3_NAME}\|${LIBE_NAME}\|${JNI4_NAME}\|${DEVICE_NAME}\|${JANSSON_NAME}\|${IOT_NAME}\|${AI_NAME}"
		;;
	"u")
		echo "Uninstall SUSI AI service."
		remove_ai_service
		echo "Uninstall SUSI."
		uninstalllibrary
		;;
	*)
		echo "ERROR: \"${1}\" is an invalid input parameter!"
		usage
		;;
esac
