from abc import ABC, abstractmethod
from typing import Type, Iterable
from result import Result, Err, Ok, is_ok
from .main import TempShot

import sensors

#
def read_sensor_by_label(chip: object, labels: Iterable or str) -> Result:
    retval = {}

    if isinstance(labels, str):
        labels = [labels]

    try:
        for feature in sensors.FeatureIterator(chip):
            for label in labels:
                if not label:
                    raise ValueError('label cant be an enpty string')

                if sensors.get_label(chip, feature) == label:
                    retval[label.replace(' ', '_').lower()] = sensors.get_value(chip, feature.number)
        return Ok(retval)

    except Exception as e:
        return Err(e)

#
class Reader(ABC):

    @abstractmethod
    def read(self):
        pass

#
class ThinkpadEXXXReader(Reader):

    # hard coded critical 
    # temp. values
    _conf = { 
        'cpu_max': 80, 
        'gpu_max': 75, 
        'hdd_max': 65, 
        'case_max': 68 
    }

    def read(self):
        rval = {}

        sensors.init()

        for chip in sensors.ChipIterator():
            chip_name = sensors.chip_snprintf_name(chip)

            if chip_name.startswith("amdgpu-pci-"):
                result = read_sensor_by_label(chip, 'GPU')
    
                rval['gpu'] = int(result.ok_value['gpu']) if is_ok(result) else -1

            elif chip_name.startswith("k10temp-pci-"):
                result = read_sensor_by_label(chip, 'CPU')

                rval['cpu'] = int(result.ok_value['cpu']) if is_ok(result) else -1

            elif chip_name.startswith("nvme-pci-"):
                result = read_sensor_by_label(chip, 'Composite')

                rval['hdd'] = int(result.ok_value['composite']) if is_ok(result) else -1

            elif chip_name.startswith("thinkpad-isa-"):
                result = read_sensor_by_label(chip, ['Fan speed', 'Case near CPU'])

                rval['case'] = int(result.ok_value['case_near_cpu']) if is_ok(result) else -1

        sensors.cleanup()

        return TempShot(**rval, **self._conf)


# find and instance capatible reader 
def get_reader(vendor: str, model: str) -> Type[Reader]:
    rval = None

    # normolize vendor and model
    vendor = vendor.lower(); model = model.lower()

    if vendor == 'lenovo' and model.startswith('thinkpad e4'):
        rval = ThinkpadEXXXReader()

    if not rval:
        raise ValueError('capatible reader not found')

    return rval
