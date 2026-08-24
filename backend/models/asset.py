from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from utils.db import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    asset_no = Column(String(64), unique=True, index=True, nullable=False)
    ip_address = Column(String(45), unique=True, nullable=False)
    hostname = Column(String(128), nullable=False)
    os_type = Column(String(64), nullable=False)
    status = Column(
        Enum("闲置", "在用", "报废", name="asset_status"),
        nullable=False,
        default="闲置"
    )
    purchase_date = Column(Date, nullable=True)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", backref="assets")
    # models/asset.py 添加字段
    ssh_user = Column(String(50), nullable=True)
    ssh_password = Column(String(255), nullable=True)   # 建议加密存储
    ssh_port = Column(Integer, default=22)