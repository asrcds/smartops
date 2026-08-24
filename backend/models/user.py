from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from utils.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False)  # 用于登录
    email = Column(String(100), nullable=True)  # 可选，用于接收通知
    hashed_password = Column(String(255), nullable=False)  # 存储加密后的密码
    role = Column(String(20), default="user", nullable=False)  # 区分管理员和普通用户
    create_time = Column(DateTime, server_default=func.now())  # 默认当前时间
    is_active = Column(Boolean, default=True, nullable=False)  # 软删除或封号
    reset_token = Column(String(100), nullable=True, default=None)  # 用于存储临时的重置令牌
    reset_token_expires = Column(DateTime, nullable=True, default=None)  # 用于存储令牌的过期时间

   
    

    def __repr__(self):
        return (f"<User(id={self.id}, username='{self.username}', email='{self.email}', "
                f"role='{self.role}', is_active={self.is_active}, create_time={self.create_time}, "
                f"reset_token={self.reset_token}, reset_token_expires={self.reset_token_expires})>")



