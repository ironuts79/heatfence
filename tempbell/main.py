from pydantic import BaseModel, ConfigDict, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
#
class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=(".env.dev", ".env"),
        env_ignore_empty=True,
        case_sensitive=False,
        extra="ignore",
    )
    #
    feed_interval: int = 10
#
class TempShot(BaseModel):
    model_config = ConfigDict(extra="forbid")

    cpu: int
    cpu_max: int = 99

    gpu: int
    gpu_max: int = 99

    hdd: int
    hdd_max: int = 99

    case: int
    case_max: int = 99

    @computed_field
    def status(self) -> str:
        if ( self.cpu >= self.cpu_max or 
             self.gpu >= self.gpu_max or 
             self.hdd >= self.hdd_max or 
             self.case >= self.case_max ):

            return 'ALARM'

        return 'NORM'
