from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from utils.db import get_db
from models.asset import Asset
from utils.response import response_success, response_error, BaseResponse
from routes.auth import get_current_user
from models.user import User
from pydantic import ConfigDict, BaseModel
router = APIRouter()

class AssetCreate(BaseModel):
    asset_no: str
    ip_address: str
    hostname: str
    os_type: str
    status: str = "闲置"
    purchase_date: Optional[str] = None
    owner_id: Optional[int] = None
class AssetUpdateStatus(BaseModel):
    status: str

class AssetOut(BaseModel):
    id: int
    asset_no: str
    ip_address: str
    hostname: str
    os_type: str
    status: str
    purchase_date: Optional[str] = None
    owner_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

@router.get("", response_model=BaseResponse)
def list_assets(
    skip: int = Query(0, ge=0, description="跳过条数"),
    limit: int = Query(10, ge=1, le=50, description="分页大小"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> BaseResponse:
    assets = db.query(Asset).offset(skip).limit(limit).all()
    # 转成 AssetOut 确保序列化兼容
    assets_out = [AssetOut.from_orm(a) for a in assets]
    return response_success(data=assets_out)
@router.post("", response_model=BaseResponse)
def create_asset(
    asset: AssetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> BaseResponse:
    # 保证资产编号唯一
    if db.query(Asset).filter(Asset.asset_no == asset.asset_no).first():
        return response_error(code=400, msg="资产编号已存在")
    db_asset = Asset(
        asset_no=asset.asset_no,
        ip_address=asset.ip_address,
        hostname=asset.hostname,
        os_type=asset.os_type,
        status=asset.status,
        purchase_date=asset.purchase_date,
        owner_id=asset.owner_id
    )
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return response_success(data=AssetOut.from_orm(db_asset))

@router.delete("{asset_id}", response_model=BaseResponse)
def delete_asset(
    asset_id: int = Path(..., description="资产ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> BaseResponse:
    db_asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="资产不存在")
    db.delete(db_asset)
    db.commit()
    return response_success(msg="删除成功")

@router.put("{asset_id}/status", response_model=BaseResponse)
def update_asset_status(
    asset_id: int = Path(..., description="资产ID"),
    status_update: AssetUpdateStatus = ...,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> BaseResponse:
    db_asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="资产不存在")
    allowed_status = ["闲置", "在用", "报废"]
    if status_update.status not in allowed_status:
        return response_error(code=400, msg=f"状态必须为 {allowed_status}")
    db_asset.status = status_update.status
    db.commit()
    db.refresh(db_asset)
    return response_success(data=AssetOut.from_orm(db_asset))
