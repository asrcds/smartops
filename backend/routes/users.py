from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from utils.db import get_db
from models import user as user_model

from pydantic import BaseModel

# 新增：统一响应
from utils.response import response_success, response_error, BaseResponse

router = APIRouter()


# ----- 权限校验的假设 -----
# 从 token 验证、获取当前用户，示意性实现，实际应该复用 auth 里的方法
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
SECRET_KEY = "your_jwt_secret_key_here"
ALGORITHM = "HS256"

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        if username is None or user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if user is None or not user.is_active:
        raise credentials_exception
    return user

def require_admin(current_user: user_model.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="仅限管理员操作。")
    return current_user

# ----- Pydantic Schemas -----
class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    role: str
    create_time: Optional[str] = None
    is_active: bool

    class Config:
        orm_mode = True

class UserRoleUpdateRequest(BaseModel):
    role: str

# 1. 获取用户列表（分页） GET /users/
@router.get("/", response_model=BaseResponse)
def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(require_admin),
) -> BaseResponse:
    offset = (page - 1) * size
    users = db.query(user_model.User).order_by(user_model.User.id).offset(offset).limit(size).all()
    # 可以加 data 返回 total 也可以只返回列表，这里保持语义为清单
    return response_success(data=[UserResponse.from_orm(user) for user in users])

# 2. 获取用户详情 GET /users/{user_id}
@router.get("/{user_id}", response_model=BaseResponse)
def user_detail(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user),
) -> BaseResponse:
    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if not user:
        return response_error(code=400, msg="用户不存在")
    return response_success(data=UserResponse.from_orm(user))

# 3. 删除用户（软删除） DELETE /users/{user_id}
@router.delete("/{user_id}", response_model=BaseResponse)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(require_admin),
) -> BaseResponse:
    if user_id == current_user.id:
        return response_error(code=400, msg="不能删除自己")
    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if not user:
        return response_error(code=400, msg="用户不存在")
    # 软删除
    user.is_active = False
    db.add(user)
    db.commit()
    return response_success(data={"msg": "用户已软删除（已禁用）"})
@router.delete("/admin/users/{user_id}")
def admin_delete_user(
    user_id: int,
    current_user: user_model.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 仅管理员允许
    if current_user.role != "admin":
        return response_error(code=403, msg="仅管理员允许")
    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if not user:
        return response_error(code=400, msg="用户不存在")
    db.delete(user)
    db.commit()
    return response_success(data={"msg": "用户已删除"})
# 4. 修改用户角色 PUT /users/{user_id}/role
@router.put("/{user_id}/role", response_model=BaseResponse)
def update_user_role(
    user_id: int,
    data: UserRoleUpdateRequest,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(require_admin),
) -> BaseResponse:
    if data.role not in ("admin", "user"):
        return response_error(code=403, msg="role 只允许 admin 或 user")
    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if not user:
        return response_error(code=404, msg="用户不存在")
    user.role = data.role
    db.add(user)
    db.commit()
    return response_success(data={"msg": f"用户角色已更新为 {data.role}"})
