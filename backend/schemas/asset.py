from typing import Optional
from datetime import datetime

from pydantic import BaseModel, constr, Field, validator

import re

class AssetBase(BaseModel):
    hostname: constr(strip_whitespace=True, min_length=1)
    ip_address: constr(strip_whitespace=True, min_length=7, max_length=45)
    os_type: str = Field(default="Linux")
    status: str = Field(default="闲置")

    @validator("ip_address")
    def validate_ip(cls, v):
        ip_regex = re.compile(
            r"^(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}"
            r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)$"
        )
        if not ip_regex.match(v):
            raise ValueError("ip_address格式不正确，应为合法IPv4地址")
        return v

class AssetCreate(AssetBase):
    pass

class AssetResponse(AssetBase):
    id: int
    create_time: datetime
    owner_username: Optional[str] = None

    class Config:
        orm_mode = True