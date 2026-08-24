from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from utils.db import Base
from sqlalchemy.orm import relationship
from models.user import User
class TaskRecord(Base):
    __tablename__ = "task_records"

    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String(255), nullable=False)
    command = Column(String(500), nullable=False)
    target_hosts = Column(JSON, nullable=False)          # 存储 IP 列表
    status = Column(String(20), default="PENDING")       # PENDING, RUNNING, SUCCESS, FAILED
    result = Column(JSON, nullable=True)                 # 存储 stdout/stderr/error
    creator_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    creator = relationship("User", backref="tasks")