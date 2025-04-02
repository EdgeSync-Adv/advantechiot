
import unittest
import advantechiot


class TestMotherboard(unittest.TestCase):
    def test_name(self):
        handler = advantechiot.Device()
        print(handler.motherboard.name)

    def test_bios_revision(self):
        handler = advantechiot.Device()
        print(handler.motherboard.bios_revision)

    def test_voltage_sources(self):
        handler = advantechiot.Device()
        print()
        for source in handler.motherboard.voltage_sources:
            print(source)

    def test_get_voltage(self):
        handler = advantechiot.Device()
        for source in handler.motherboard.voltage_sources:
            print(f"{source}: {handler.motherboard.get_voltage(source)}V")

    def test_temperature_sources(self):
        handler = advantechiot.Device()
        for source in handler.motherboard.temperature_sources:
            print(source)

    def test_get_temperature(self):
        handler = advantechiot.Device()
        print()
        for source in handler.motherboard.temperature_sources:
            print(f"{source}: {handler.motherboard.get_temperature(source)} degrees Celsius")


class TestGpio(unittest.TestCase):
    def test_get_gpio_direction(self):
        handler = advantechiot.Device()
        print()
        print(handler.gpio.pins)
        for i in range(handler.gpio.gpio_counter):
            print(f"GPIO{i}, direction:{handler.gpio.get_gpio_direction(i)}")

    def test_get_gpio_level(self):
        handler = advantechiot.Device()
        print()
        print(handler.gpio.pins)
        for i in range(handler.gpio.gpio_counter):
            print(f"GPIO{i}, level:{handler.gpio.get_gpio_level(i)}")


class TestMemory(unittest.TestCase):
    def test_memory_count(self):
        handler = advantechiot.Device()
        print(f"memory count: {handler.memory.memory_count}")

    def test_get_memory_type(self):
        handler = advantechiot.Device()
        for i in range(handler.memory.memory_count):
            print(
                f"memory{i} type:{handler.memory.get_memory_type(i)}")

    def test_get_module_type(self):
        handler = advantechiot.Device()
        for i in range(handler.memory.memory_count):
            print(
                f"memory{i} module type:{handler.memory.get_module_type(i)}")

    def test_get_memory_size_in_GB(self):
        handler = advantechiot.Device()
        for i in range(handler.memory.memory_count):
            print(
                f"memory{i} size in GB:{handler.memory.get_memory_size_in_GB(i)}")

    def test_get_memory_speed(self):
        handler = advantechiot.Device()
        for i in range(handler.memory.memory_count):
            print(
                f"memory{i} speed:{handler.memory.get_memory_speed(i)}")

    def test_get_memory_rank(self):
        handler = advantechiot.Device()
        for i in range(handler.memory.memory_count):
            print(
                f"memory{i} rank:{handler.memory.get_memory_rank(i)}")

    def test_get_memory_voltage(self):
        handler = advantechiot.Device()
        for i in range(handler.memory.memory_count):
            print(
                f"memory{i} voltage:{handler.memory.get_memory_voltage(i)} v")

    def test_get_memory_bank(self):
        handler = advantechiot.Device()
        for i in range(handler.memory.memory_count):
            print(
                f"memory{i} bank:{handler.memory.get_memory_bank(i)}")

    def test_get_memory_manufacturing_date_code(self):
        handler = advantechiot.Device()
        for i in range(handler.memory.memory_count):
            print(
                f"memory{i} manufacturing date code week/year:{handler.memory.get_memory_manufacturing_date_code(i)}")

    def test_get_memory_temperature(self):
        handler = advantechiot.Device()
        for i in range(handler.memory.memory_count):
            print(
                f"memory{i} temperature:{handler.memory.get_memory_temperature(i)} degrees Celsius")

    def test_get_memory_write_protection(self):
        handler = advantechiot.Device()
        for i in range(handler.memory.memory_count):
            print(
                f"memory{i} write protection:{handler.memory.get_memory_write_protection(i)}")

    def test_get_memory_module_manufacture(self):
        handler = advantechiot.Device()
        for i in range(handler.memory.memory_count):
            print(
                f"memory{i} module manufacture:{handler.memory.get_memory_module_manufacture(i)}")

    def test_get_memory_manufacture(self):
        handler = advantechiot.Device()
        for i in range(handler.memory.memory_count):
            print(
                f"memory{i} manufacture:{handler.memory.get_memory_manufacture(i)}")

    def test_get_memory_part_number(self):
        handler = advantechiot.Device()
        for i in range(handler.memory.memory_count):
            print(
                f"memory{i} part number:{handler.memory.get_memory_part_number(i)}")

    def test_get_memory_specific(self):
        handler = advantechiot.Device()
        for i in range(handler.memory.memory_count):
            print(
                f"memory{i} specific:{handler.memory.get_memory_specific(i)}")


class TestDisk(unittest.TestCase):
    def test_total_disk_space(self):
        handler = advantechiot.Device()
        print(f"Total Disk Space: {handler.disk.total_disk_space}")

    def test_free_disk_space(self):
        handler = advantechiot.Device()
        print(f"Free Disk Space: {handler.disk.free_disk_space}")


if __name__ == '__main__':
    unittest.main()
