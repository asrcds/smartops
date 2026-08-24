# backend/models/__init__.py

# 从 database 模块导入 Base，并在这里重新导出
# 这样其他文件就可以写 from models import Base 了
from utils.db import Base

# 同时，建议在这里导入所有模型类，触发它们的注册机制
# 这一步非常关键！如果不导入，Base 就不知道有这些表的存在
from .user import User
from .asset import Asset
from .task import TaskRecord
from .log import OperationLog, SystemLog

# 定义 __all__ 方便外部导入
__all__ = ["Base", "User", "Asset", "TaskRecord", "OperationLog", "SystemLog"]