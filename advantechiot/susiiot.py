import ctypes
import json
import sys
import os
import platform
from .imotherboard import IMotherboard
from .igpio import IGpio, GpioDirectionType, GpioLevelType
from .imemory import IMemory
from .idisk import IDisk
from typing import List


class SusiIot(IMotherboard, IGpio, IMemory, IDisk):
    def __init__(self):
        self.susi_iot_library = None
        self.json_library = None
        self.susi_information = None
        self.gpio_list = []
        self.memory_list = []
        self.voltage_source_list = []
        self.temperature_source_list = []
        self.susi_id_name_table = {}
        self.susi_name_id_table = {}

        self.check_root_authorization()
        self.import_library()
        self.initialize_library()
        self.susi_iot_library.SusiIoTInitialize()
        self.get_susi_information_string()
        self.get_gpio_list()
        self.get_sdram_list()
        self.get_name_id_list()

    def __del__(self):
        pass
        # self.susi_iot_library.SusiIoTUninitialize()

    def check_root_authorization(self):
        if os.geteuid() != 0:
            sys.exit("Error: Please run this program as root (use sudo).")
        else:
            return True

    def read_mock_data(self, data):
        self.susi_information = data

    def set_id_and_name_table(self):
        self.susi_name_id_table.update({"Platform Information": 65536})
        self.susi_name_id_table.update({"Board manufacturer": 16843777})
        self.susi_name_id_table.update({"Board name": 16843778})
        self.susi_name_id_table.update({"BIOS revision": 16843781})
        self.susi_name_id_table.update({"Driver version": 16843265})
        self.susi_name_id_table.update({"Library version": 16843266})
        self.susi_name_id_table.update({"Hardware Monitor": 131072})
        self.susi_name_id_table.update({"Voltage Vcore": 16908801})
        self.susi_name_id_table.update({"Voltage 3.3V": 16908804})
        self.susi_name_id_table.update({"Voltage 5V": 16908805})
        self.susi_name_id_table.update({"Voltage 12V": 16908806})
        self.susi_name_id_table.update({"Voltage 5V Standby": 16908807})
        self.susi_name_id_table.update({"Voltage CMOS Battery": 16908809})
        self.susi_name_id_table.update({"Voltage VCC3V": 16908817})
        self.susi_name_id_table.update({"Temperature CPU": 16908545})
        self.susi_name_id_table.update({"Temperature System": 16908547})
        self.susi_name_id_table.update({"Fan Speed CPUFAN1": 16909057})
        self.susi_name_id_table.update({"Fan Speed SYSFAN1": 16909058})
        self.susi_name_id_table.update({"Fan Speed SYSFAN2": 16909060})
        self.susi_name_id_table.update({"GPIO": 262144})
        self.susi_name_id_table.update({"SDRAM": 337117184})
        self.susi_name_id_table.update({"DiskInfo": 353697792})
        self.susi_name_id_table.update(
            {"Disk -volume Total Disk Space": 353697792})
        self.susi_name_id_table.update(
            {"Disk -volume Free Disk Space": 353697793})
        self.susi_name_id_table.update(
            {"Disk -etc-board Total Disk Space": 353698048})
        self.susi_name_id_table.update(
            {"Disk -etc-board Free Disk Space": 353698049})
        self.susi_name_id_table.update(
            {"Disk -etc-resolv.conf Total Disk Space": 353698304})
        self.susi_name_id_table.update(
            {"Disk -etc-resolv.conf Free Disk Space": 353698305})
        self.susi_name_id_table.update(
            {"Disk -etc-hostname Total Disk Space": 353698560})
        self.susi_name_id_table.update(
            {"Disk -etc-hostname Free Disk Space": 353698561})
        self.susi_name_id_table.update(
            {"Disk -etc-hosts Total Disk Space": 353698816})
        self.susi_name_id_table.update(
            {"Disk -etc-hosts Free Disk Space": 353698817})
        self.susi_name_id_table.update({"SUSIIoT Information": 256})
        self.susi_name_id_table.update({"SUSIIoT version": 257})
        self.susi_name_id_table.update({"Backlight": 327680})
        self.susi_name_id_table.update({"Backlight Brightness": 17106177})
        self.susi_name_id_table.update({"Backlight Frequency": 17105409})
        self.susi_name_id_table.update({"Backlight Polarity": 17105665})

    def get_name_id_list(self):
        data_sort = "Platform Information"
        try:
            id_value = self.susi_information[data_sort]["id"]
            self.susi_id_name_table.update({data_sort: id_value})
            for item in self.susi_information[data_sort]["e"]:
                self.susi_id_name_table.update({item["n"]: item["id"]})
        except:
            pass

        data_sort = "Hardware Monitor"
        try:
            id_value = self.susi_information[data_sort]["id"]
            self.susi_id_name_table.update({data_sort: id_value})
            for item in self.susi_information[data_sort]:
                if "id" in item or "bn" in item:
                    pass
                else:
                    sources = self.susi_information[data_sort][item]['e']
                    for source in sources:
                        self.susi_id_name_table.update(
                            {item+" "+source["n"]: source["id"]})
        except:
            pass

        data_sort = "Voltage"
        try:
            for key in self.susi_id_name_table.keys():
                if data_sort in key:
                    self.voltage_source_list.append(key)
        except:
            pass

        data_sort = "Temperature"
        try:
            for key in self.susi_id_name_table.keys():
                if data_sort in key:
                    self.temperature_source_list.append(key)
        except:
            pass

        data_sort = "GPIO"
        try:
            id_value = self.susi_information[data_sort]["id"]
            self.susi_id_name_table.update({data_sort: id_value})
            for data_index in self.susi_information[data_sort].keys():
                if "GPIO" in data_index:
                    self.susi_id_name_table.update(
                        {data_index: self.susi_information[data_sort][data_index]["id"]})
                    for informations in self.susi_information[data_sort][data_index]["e"]:
                        self.susi_id_name_table.update(
                            {data_index+" "+informations["n"]: informations["id"]})
        except:
            pass

        data_sort = "SDRAM"
        try:
            id_value = self.susi_information[data_sort]["id"]
            self.susi_id_name_table.update({data_sort: id_value})
            for data_index in self.susi_information[data_sort].keys():
                if "SDRAM" in data_index:
                    self.susi_id_name_table.update(
                        {data_index: self.susi_information[data_sort][data_index]["id"]})
                    for informations in self.susi_information[data_sort][data_index]["e"]:
                        self.susi_id_name_table.update(
                            {data_index+" "+informations["n"]: informations["id"]})
        except:
            pass

        data_sort = "DiskInfo"
        try:
            id_value = self.susi_information[data_sort]["id"]
            self.susi_id_name_table.update({data_sort: id_value})
            for data_index in self.susi_information[data_sort]["e"]:
                self.susi_id_name_table.update(
                    {data_index["n"]: data_index["id"]})
        except:
            pass

        data_sort = "SUSIIoT Information"
        try:
            id_value = self.susi_information[data_sort]["id"]
            self.susi_id_name_table.update({data_sort: id_value})
            for data_index in self.susi_information[data_sort]["e"]:
                self.susi_id_name_table.update(
                    {data_index["n"]: data_index["id"]})
        except:
            pass

        data_sort = "M2Talk"
        try:
            id_value = self.susi_information[data_sort]["id"]
            self.susi_id_name_table.update({data_sort: id_value})
            for data_index in self.susi_information[data_sort].keys():
                if "Device" in data_index:
                    sources = self.susi_information[data_sort][data_index]['e']
                    for source in sources:
                        self.susi_id_name_table.update(
                            {data_sort+" "+source['n']: source['id']})
        except:
            pass

        data_sort = "Backlight"
        try:
            id_value = self.susi_information[data_sort]["id"]
            self.susi_id_name_table.update({data_sort: id_value})
            for data_index in self.susi_information[data_sort].keys():
                if "Backlight" in data_index:
                    sources = self.susi_information[data_sort][data_index]['e']
                    for source in sources:
                        self.susi_id_name_table.update(
                            {data_sort+" "+source['n']: source['id']})
        except:
            pass

    def import_library(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))+"/"
        architecture = platform.machine()
        os_name = platform.system()
        susi_iot_library_path = ""
        json_library_path = ""

        if os_name == "Linux" and 'x86' in architecture.lower():
            # susi_iot_library_path = current_dir+"libSusiIoT.x86.so"
            # json_library_path = current_dir+"libjansson.x86.so"
            susi_iot_library_path = "/usr/lib/libSusiIoT.so"
            json_library_path = "/usr/lib/x86_64-linux-gnu/libjansson.so.4"

        elif os_name == "Linux" and 'aarch64' in architecture.lower():
            # susi_iot_library_path = current_dir+"libSusiIoT.arm.so"
            # json_library_path = current_dir+"libjansson.arm.so"
            susi_iot_library_path = "/lib/libSusiIoT.so"
            json_library_path = "/lib/aarch64-linux-gnu/libjansson.so.4"

        elif os_name == "Windows" and 'x86' in architecture.lower():
            pass

        elif os_name == "Windows" and 'aarch64' in architecture.lower():
            pass

        else:
            print(
                f"disable to import library, architechture:{architecture.lower()}, os:{os_name}")

        self.json_library = ctypes.CDLL(
            json_library_path, mode=ctypes.RTLD_GLOBAL)
        self.susi_iot_library = ctypes.CDLL(
            susi_iot_library_path, mode=ctypes.RTLD_GLOBAL)

    def initialize_library(self):
        SusiIoTStatus_t = ctypes.c_int
        SusiIoTId_t = ctypes.c_int

        self.susi_iot_library.SusiIoTInitialize.restype = ctypes.c_int

        self.susi_iot_library.SusiIoTSetValue.argtypes = [
            ctypes.c_uint32, ctypes.POINTER(JsonT)]
        self.susi_iot_library.SusiIoTSetValue.restype = ctypes.c_uint32

        self.susi_iot_library.SusiIoTGetLoggerPath.restype = ctypes.c_char_p

        self.susi_iot_library.SusiIoTGetPFDataString.restype = ctypes.c_char_p
        self.susi_iot_library.SusiIoTGetPFDataString.argtypes = [
            ctypes.c_uint32]

        self.susi_iot_library.SusiIoTGetPFDataStringByUri.restype = ctypes.c_char_p
        self.susi_iot_library.SusiIoTGetPFDataStringByUri.argtypes = [
            ctypes.c_char_p]

        self.json_library.json_dumps.restype = ctypes.c_char_p
        self.json_library.json_integer.restype = ctypes.POINTER(JsonT)

        self.json_library.json_real.restype = ctypes.POINTER(JsonT)
        self.json_library.json_string.restype = ctypes.POINTER(JsonT)
        prototype = ctypes.CFUNCTYPE(
            ctypes.c_char_p
        )
        self.SusiIoTGetPFCapabilityString = prototype(
            ("SusiIoTGetPFCapabilityString", self.susi_iot_library))

        self.susi_iot_library.SusiIoTUninitialize.restype = ctypes.c_int

    def get_gpio_list(self):
        try:
            for key in self.susi_information["GPIO"].keys():
                if "GPIO" in key:
                    self.gpio_list.append(key)
        except:
            pass

    def get_sdram_list(self):
        try:
            for key in self.susi_information["SDRAM"].keys():
                if "SDRAM" in key:
                    self.memory_list.append(key)
        except:
            pass

    def get_json_indent(self, n):
        json_max_indent = 0x1F
        return n & json_max_indent

    def get_json_real_precision(self, n):
        return ((n & 0x1F) << 11)

    def turn_byte_to_json(self, json_bytes):
        json_str = json_bytes.decode('utf-8')
        data = json.loads(json_str)
        return data

    def get_data_by_id(self, device_id):
        result = self.susi_iot_library.SusiIoTGetPFDataString(device_id)
        return self.turn_byte_to_json(result)

    def set_value(self, device_id, value):
        result_ptr = self.json_library.json_integer(value)
        result = result_ptr.contents
        return self.susi_iot_library.SusiIoTSetValue(device_id, result)

    def get_susi_information_string(self):
        capability_string = self.SusiIoTGetPFCapabilityString()
        capability_string = capability_string.decode('utf-8')
        try:
            self.susi_information = json.loads(capability_string)
        except json.JSONDecodeError as e:
            print("Failed to parse JSON.:", e)
        return self.susi_information

    def get_susi_information(self):
        json_max_indent = 0x1F
        jsonObject = self.json_library.json_object()
        if self.susi_iot_library.SusiIoTGetPFCapability(jsonObject) != 0:
            self.susi_information = "SusiIoTGetPFCapability failed."
            exit(1)
        else:
            self.susi_json_t = self.json_library.json_dumps(jsonObject, self.get_json_indent(
                4) | json_max_indent | self.get_json_real_precision(10))
            self.susi_information = self.turn_byte_to_json(self.susi_json_t)

        return self.susi_information

    @property
    def susi_iot_information(self):
        return self.susi_information

    @property
    def boot_up_times(self):
        try:
            id_number = self.susi_id_name_table["Boot up times"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result["v"]
        except:
            return None

    @property
    def running_time_in_hours(self):
        try:
            id_number = self.susi_id_name_table["Running time (hours)"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result["v"]
        except:
            return None

    @property
    def board_name(self):
        try:
            id_number = self.susi_id_name_table["Board name"]
            return self.get_data_by_id(id_number)["sv"]
        except:
            return None

    @property
    def bios_revision(self):
        try:
            id_number = self.susi_id_name_table["BIOS revision"]
            return self.get_data_by_id(id_number)["sv"]
        except:
            return None

    @property
    def firmware_name(self):
        try:
            id_number = self.susi_id_name_table["Firmware Name"]
            return self.get_data_by_id(id_number)["sv"]
        except:
            return None

    @property
    def library_version(self):
        try:
            id_number = self.susi_id_name_table["Driver version"]
            return self.get_data_by_id(id_number)["sv"]
        except:
            return None

    @property
    def driver_version(self):
        try:
            id_number = self.susi_id_name_table["Driver version"]
            return self.get_data_by_id(id_number)["sv"]
        except:
            return None

    @property
    def firmware_version(self):
        try:
            id_number = self.susi_id_name_table["Firmware version"]
            return self.get_data_by_id(id_number)["sv"]
        except:
            return None

    @property
    def voltage_vcore(self):
        try:
            id_number = self.susi_id_name_table["Voltage Vcore"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result["v"]
        except:
            return None

    @property
    def voltage_3p3v(self):
        try:
            id_number = self.susi_id_name_table["Voltage 3.3V"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result["v"]
        except:
            return None

    @property
    def voltage_5v(self):
        try:
            id_number = self.susi_id_name_table["Voltage 5V"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result["v"]
        except:
            return None

    @property
    def voltage_12v(self):
        try:
            id_number = self.susi_id_name_table["Voltage 12V"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result["v"]
        except:
            return None

    @property
    def voltage_5v_standby(self):
        try:
            id_number = self.susi_id_name_table["Voltage 5V Standby"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result["v"]
        except:
            return None

    @property
    def voltage_cmos_battery(self):
        try:
            id_number = self.susi_id_name_table["Voltage CMOS Battery"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result["v"]
        except:
            return None

    @property
    def dc_power(self):
        try:
            id_number = self.susi_id_name_table["Voltage DC"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result["v"]
        except:
            return None

    @property
    def cpu_temperature_in_celsius(self):
        try:
            id_number = self.susi_id_name_table["Temperature System"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result["v"]
        except:
            return None

    @property
    def system_temperature_in_celsius(self):
        try:
            id_number = self.susi_id_name_table["Temperature System"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result["v"]
        except:
            return None

    @property
    def gpio_counter(self):
        return len(self.gpio_list)

    def get_gpio_direction(self, gpio_number=0):
        try:
            gpio_string = self.gpio_list[gpio_number]
            id_number = self.susi_information["GPIO"][gpio_string]["e"][0]["id"]
            return self.get_data_by_id(id_number)['bv']
        except:
            return None

    def set_gpio_direction(self, gpio_number=0, direction=0):
        try:
            gpio_string = self.gpio_list[gpio_number]
            id_number = self.susi_information["GPIO"][gpio_string]["e"][0]["id"]
            result = self.set_value(id_number, direction)
            if result != 0:
                return False
            return True
        except:
            return None

    def get_gpio_level(self, gpio_number=0):
        try:
            gpio_string = self.gpio_list[gpio_number]
            id_number = self.susi_information["GPIO"][gpio_string]["e"][1]["id"]
            return self.get_data_by_id(id_number)['bv']
        except:
            return None

    def is_gpio_output(self, gpio_number=0):
        try:
            gpio_string = self.gpio_list[gpio_number]
            id_number = self.susi_information["GPIO"][gpio_string]["e"][0]["id"]
            if self.get_data_by_id(id_number)['bv'] == 0:
                return True
        except:
            return False

    def is_gpio_output_with_gpio_name(self, gpio_name=0):
        try:
            id_number = self.susi_information["GPIO"][gpio_name]["e"][0]["id"]
            if self.get_data_by_id(id_number)['bv'] == 0:
                return True
        except:
            return False

    def set_gpio_level(self, gpio_number=0, level=0):
        gpio_direction_is_output = self.is_gpio_output(gpio_number)
        if not gpio_direction_is_output:
            return False
        gpio_string = self.gpio_list[gpio_number]
        id_number = self.susi_information["GPIO"][gpio_string]["e"][1]["id"]
        result = self.set_value(id_number, level)
        if result != 0:
            return False
        return True

    @property
    def memory_count(self):
        return len(self.memory_list)

    def get_memory_type(self, memory_number=0):
        try:
            memory_name = self.memory_list[memory_number]
            id_number = self.susi_id_name_table[memory_name+" "+"Memory Type"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result['sv']
        except:
            return None

    def get_module_type(self, memory_number=0):
        try:
            memory_name = self.memory_list[memory_number]
            id_number = self.susi_id_name_table[memory_name+" "+"Module Type"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result['sv']
        except:
            return None

    def get_memory_size_in_GB(self, memory_number=0):
        try:
            memory_name = self.memory_list[memory_number]
            id_number = self.susi_id_name_table[memory_name+" "+"Module Size"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result['v']
        except:
            return None

    def get_memory_speed(self, memory_number=0):
        try:
            memory_name = self.memory_list[memory_number]
            id_number = self.susi_id_name_table[memory_name+" "+"Memory Speed"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result['sv']
        except:
            return None

    def get_memory_rank(self, memory_number=0):
        try:
            memory_name = self.memory_list[memory_number]
            id_number = self.susi_id_name_table[memory_name+" "+"Rank"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result['v']
        except:
            return None

    def get_memory_voltage(self, memory_number=0):
        try:
            memory_name = self.memory_list[memory_number]
            id_number = self.susi_id_name_table[memory_name+" "+"Voltage"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result['v']
        except:
            return None

    def get_memory_bank(self, memory_number=0):
        try:
            memory_name = self.memory_list[memory_number]
            id_number = self.susi_id_name_table[memory_name+" "+"Bank"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result['sv']
        except:
            return None

    def get_memory_manufacturing_date_code(self, memory_number=0):
        try:
            memory_name = self.memory_list[memory_number]
            id_number = self.susi_id_name_table[memory_name+" "+"Week Year"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result['sv']
        except:
            return None

    def get_memory_temperature(self, memory_number=0):
        try:
            memory_name = self.memory_list[memory_number]
            id_number = self.susi_id_name_table[memory_name+" "+"Temperature"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result['v']
        except:
            return None

    def get_memory_write_protection(self, memory_number=0):
        try:
            memory_name = self.memory_list[memory_number]
            id_number = self.susi_id_name_table[memory_name +
                                                " "+"Write Protection"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result['sv']
        except:
            return None

    def get_memory_module_manufacture(self, memory_number=0):
        try:
            memory_name = self.memory_list[memory_number]
            id_number = self.susi_id_name_table[memory_name +
                                                " "+"Module Manufacture"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result['sv']
        except:
            return None

    def get_memory_manufacture(self, memory_number=0):
        try:
            memory_name = self.memory_list[memory_number]
            id_number = self.susi_id_name_table[memory_name +
                                                " "+"DRAM Manufacture"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result['sv']
        except:
            return None

    def get_memory_part_number(self, memory_number=0):
        try:
            memory_name = self.memory_list[memory_number]
            id_number = self.susi_id_name_table[memory_name+" "+"Part Number"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result['sv']
        except:
            return None

    def get_memory_specific(self, memory_number=0):
        try:
            memory_name = self.memory_list[memory_number]
            id_number = self.susi_id_name_table[memory_name +
                                                " "+"Specific Data"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result['sv']
        except:
            return None

    @property
    def total_disk_space(self):
        # todo, there are 2 item with the same id 353697792
        try:
            id_number = 353697792
            result = self.get_data_by_id(id_number)
            result = result['e'][0]
            if not result:
                print(f"{id_number} result is {result}")
            return result["v"]
        except:
            return None

    @property
    def free_disk_space(self):
        try:
            id_number = 353697793
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result["v"]
        except:
            return None

    @property
    def cpu_fan_speed(self):
        try:
            id_number = self.susi_id_name_table["Fan Speed CPU"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result["v"]
        except:
            return None

    @property
    def system_fan_speed(self):
        try:
            id_number = self.susi_id_name_table["Fan Speed System"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result["v"]
        except:
            return None

    @property
    def susiiot_version(self):
        try:
            id_number = self.susi_id_name_table["version"]
            return self.get_data_by_id(id_number)["sv"]
        except:
            return None

    @property
    def backlight_frequency(self):
        try:
            id_number = self.susi_id_name_table["Backlight frequency"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result["v"]
        except:
            return None

    @property
    def backlight_polarity(self):
        try:
            id_number = self.susi_id_name_table["Backlight polarity"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result["v"]
        except:
            return None

    @property
    def backlight_backlight(self):
        try:
            id_number = self.susi_id_name_table["Backlight backlight"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result["v"]
        except:
            return None

    @property
    def backlight_brightness(self):
        try:
            id_number = self.susi_id_name_table["Backlight brightness"]
            result = self.get_data_by_id(id_number)
            if not result:
                print(f"{id_number} result is {result}")
            return result["v"]
        except:
            return None

    @property
    def name(self) -> str:
        try:
            for item in self.susi_information["Platform Information"]["e"]:
                if item["n"] == "Board name":
                    return item["sv"]
            return None
        except:
            return None

    @property
    def bios_revision(self) -> str:
        try:
            for item in self.susi_information["Platform Information"]["e"]:
                if item["n"] == "BIOS revision":
                    return item["sv"]
            return None
        except:
            return None

    @property
    def voltage_sources(self) -> List[str]:
        return self.voltage_source_list

    @property
    def temperature_sources(self) -> List[str]:
        return self.temperature_source_list

    def get_voltage(self, voltage_source) -> float:
        try:
            id_number = self.susi_id_name_table[voltage_source]
            result = self.get_data_by_id(id_number)
            return float(result["v"])
        except:
            pass

    def get_temperature(self, temperature_source) -> float:
        try:
            id_number = self.susi_id_name_table[temperature_source]
            result = self.get_data_by_id(id_number)
            return float(result["v"])
        except:
            pass

    @property
    def fan_source(self) -> List[str]:
        pass

    def get_fan_speed(self, fan_source) -> int:
        pass

    @property
    def pins(self) -> List[str]:
        return self.gpio_list

    def get_direction(self, pin: str) -> None:
        try:
            id_number = self.susi_information["GPIO"][pin]["e"][0]["id"]
            return self.get_data_by_id(id_number)['bv']
        except:
            return None

    def set_direction(self, pin: str, direction: GpioDirectionType) -> None:
        try:
            id_number = self.susi_information["GPIO"][pin]["e"][0]["id"]
            result = self.set_value(id_number, direction)
            if result != 0:
                return False
            return True
        except:
            return None

    def get_level(self, pin: str) -> None:
        try:
            id_number = self.susi_information["GPIO"][pin]["e"][1]["id"]
            return self.get_data_by_id(id_number)['bv']
        except:
            return None

    def set_level(self, pin: str, level: GpioLevelType) -> None:
        gpio_direction_is_output = self.is_gpio_output_with_gpio_name(pin)
        if not gpio_direction_is_output:
            return False
            id_number = self.susi_information["GPIO"][pin]["e"][1]["id"]
            result = self.set_value(id_number, level)
            if result != 0:
                return False
        return True


class JsonType:
    JSON_OBJECT = 0
    JSON_ARRAY = 1
    JSON_STRING = 2
    JSON_INTEGER = 3
    JSON_REAL = 4
    JSON_TRUE = 5
    JSON_FALSE = 6
    JSON_NULL = 7


class JsonT(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_int),
        ("refcount", ctypes.c_size_t)
    ]
