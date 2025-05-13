from typing import Literal, Optional
from pydantic import ( BaseModel, 
                       ConfigDict,
                       field_validator,
                       computed_field )

import logging

logger = logging.getLogger('TermSlice')

#
class TempSlice(BaseModel):
    model_config = ConfigDict(extra="forbid")

    cpu: int
    cpu_max: int

    gpu: int
    gpu_max: int

    hdd: int
    hdd_max: int

    cassis: int
    cassis_max: int

    battery: int
    battery_max: int

    alarm_reason: str = ''
    
    #
    @field_validator ('cpu', 'gpu', 'hdd', 'cassis', 'battery', mode='before')
    def validate_temperature(t: int) -> Optional[int]:
        return t if (t >= 0 and t < 100) else None
  
    #
    @computed_field
    def status(self) -> Literal['ok', 'alarm']:
    
        # flush alarm
        self.alarm_reason = ''

        if self.cpu_max != 0 and self.cpu >= self.cpu_max:
            self.alarm_reason = "CPU temperature is too hight val: {}C, max: {}C".format(self.cpu, self.cpu_max)

        if self.gpu_max != 0 and self.gpu >= self.gpu_max:
            self.alarm_reason = "GPU temperature is too hight val: {}C, max: {}C".format(self.gpu, self.gpu_max)

        if self.hdd_max != 0 and self.hdd >= self.hdd_max:
            self.alarm_reason = "HDD temp. is too hight val: {}C, max: {}C".format(self.hdd, self.hdd_max)

        if self.cassis_max != 0 and self.cassis >= self.cassis_max:
            self.alarm_reason = "cassis temp. is too hight val: {}C, max: {}C".format(self.cassis, self.cassis_max)

        if self.battery_max != 0 and self.battery >= self.battary_max:
            self.alarm_reason = "battery temp. is too hight val: {}C, max: {}C".format(self.battery, self.battery_max)

        # ok (no alaram) if reason 
        # value is emplty string
        return 'alarm' if self.alarm_reason else 'ok'