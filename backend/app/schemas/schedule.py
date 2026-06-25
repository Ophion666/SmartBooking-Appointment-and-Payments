from enum import Enum
from pydantic import BaseModel, ConfigDict
from datetime import time

class DayOfWeek(str, Enum):

    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"
    Sunday = "Sunday"

class ScheduleCreate (BaseModel):

    master_id: int
    day_of_week: DayOfWeek
    start_time: time
    end_time: time

class ScheduleResponse(BaseModel):

    id: int
    master_id: int
    day_of_week: DayOfWeek
    start_time: time
    end_time: time

    model_config = ConfigDict(from_attributes=True)