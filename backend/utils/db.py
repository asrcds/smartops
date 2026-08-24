from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import settings

Base = declarative_base()

# 先创建 engine
engine = create_engine(
    settings.get_database_url(),
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={"charset": "utf8mb4"},
)

# 导入所有模型（确保它们被注册到 Base.metadata）
# 方式1：如果模型在 models 包中且 __init__.py 已导出
from models import User, Asset, TaskRecord, OperationLog, SystemLog  # 根据实际模型名修改
# 或者直接导入整个包（如果 __init__.py 中有导入语句）
# import models

# 创建所有表
Base.metadata.create_all(bind=engine)

# 会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()