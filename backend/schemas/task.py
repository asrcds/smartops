from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, constr

class TaskCreate(BaseModel):
    command: constr(strip_whitespace=True, min_length=1)
    target_host_ids: List[int]

class TaskResponse(BaseModel):
    id: int
    task_name: str
    status: str
    create_time: datetime
    result: Optional[str] = None

    class Config:
        orm_mode = True