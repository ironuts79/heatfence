from result import is_ok
from .abc import Reader
from .sensor import read_sensor_by_label

import sensors
#
class ThinkpadT4XXReader(Reader):
    _limits = { 'cpu_max': 80,
                'gpu_max': 60,
                'hdd_max': 60,
                'cassis_max': 0,
                'battery_max': 0 }

    def _read(self) -> dict:
        retval = { 
            'battery': 0 
        }

        sensors.init()

        self.logger.info("read values of thermal sensors")

        for chip in sensors.ChipIterator():
            chip_name = sensors.chip_snprintf_name(chip)

            if chip_name.startswith("amdgpu-pci-"):
                result = read_sensor_by_label(chip, 'GPU')

                if is_ok(result): 
                    retval['gpu'] = int(result.ok_value['gpu'])
                    self.logger.debug("read GPU temperature {}C from [{}]".format(retval['gpu'], chip_name))

            elif chip_name.startswith("k10temp-pci-"):
                result = read_sensor_by_label(chip, 'CPU')

                if is_ok(result):
                    retval['cpu'] = int(result.ok_value['cpu'])
                    self.logger.debug("read CPU temperature {}C from [{}]".format(retval['cpu'], chip_name))

            elif chip_name.startswith("nvme-pci-"):
                result = read_sensor_by_label(chip, 'Composite')

                if is_ok(result): 
                    retval['hdd'] = int(result.ok_value['composite'])
                    self.logger.debug("read HDD temperature {}C from [{}]".format(retval['hdd'], chip_name))

            elif chip_name.startswith("thinkpad-isa-"):
                result = read_sensor_by_label(chip, ['Fan speed', 'Case near CPU'])

                if is_ok(result): 
                    retval['cassis'] = int(result.ok_value['case_near_cpu'])
                    self.logger.debug("read Cassis temperature near CPU {}C from [{}]".format(retval['cassis'], chip_name))

        sensors.cleanup()

        return retval

# thinkpad E4XX reader
class ThinkpadE4XXReader(ThinkpadT4XXReader):
    _limits = { 'cpu_max': 10,
                'gpu_max': 68,
                'hdd_max': 70,
                'cassis_max': 70,
                'battery_max': 0 }