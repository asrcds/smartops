from typing import Any, Optional
from pydantic import BaseModel

class BaseResponse(BaseModel):
    code: int                           # 状态码（200 表示成功，其它为业务错误）
    msg: str                            # 提示信息
    data: Optional[Any] = None          # 业务数据，任意类型

def response_success(data: Any = None, msg: str = "操作成功") -> BaseResponse:
    return BaseResponse(code=200, msg=msg, data=data)

def response_error(code: int = 400, msg: str = "操作失败") -> BaseResponse:
    return BaseResponse(code=code, msg=msg, data=None)

class APIException(Exception):
    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg
        super().__init__(f"APIException {code}: {msg}")
