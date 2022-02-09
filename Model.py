from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime as dt


class ModuleData(BaseModel):
    AmbientTemperature: Optional[float] = None
    StorageTemperature: float
    LDRStatus: Optional[int] = None
    ReleState: Optional[int] = None
    Timestamp: dt
    ModuleID: Optional[int] = None


class ModuleDataOld(BaseModel):
    Temperature: float
    LDR: Optional[int] = None
    ReleState: Optional[int] = None
    Timestamp: dt
    ModuleID: Optional[int] = None
    mod_id: Optional[int] = None


class DateRange(BaseModel):
    StartDate: str = "2022-02-01 20:00:00"
    EndDate: str = "2022-02-05 20:00:00"
