from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, func
from utils.db import Base

class OperationLog(Base):
    __tablename__ = "operation_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    username = Column(String(64), nullable=False)
    action = Column(String(64), nullable=False)  # e.g. "登录", "添加资产", "执行命令"
    ip_address = Column(String(45), nullable=False)
    status = Column(Enum("成功", "失败", name="operation_status"), nullable=False)
    create_time = Column(DateTime, server_default=func.now())

class SystemLog(Base):
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True, index=True)
    server_ip = Column(String(45), nullable=False)
    level = Column(Enum("ERROR", "WARNING", "INFO", name="log_level"), nullable=False)
    message = Column(String(1024), nullable=False)
    create_time = Column(DateTime, server_default=func.now())