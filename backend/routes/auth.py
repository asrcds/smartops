from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import secrets
from pydantic import BaseModel, EmailStr
from typing import Optional
import traceback

from utils.db import get_db
from models.user import User
from config import settings
from utils.response import response_success, response_error, BaseResponse

router = APIRouter()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# 数据模型
class UserRegister(BaseModel):
    username: str
    password: str
    email: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# 工具函数
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "sub": str(data.get("sub"))})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user


# API 路由
@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """用户登录"""
    try:
        # 查找用户
        user = db.query(User).filter(User.username == form_data.username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 验证密码
        if not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 生成访问令牌
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"登录异常: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="服务器内部错误"
        )


@router.post("/register", response_model=BaseResponse)
def register(user: UserRegister, db: Session = Depends(get_db)) -> BaseResponse:
    """用户注册"""
    try:
        print(f"注册请求: username={user.username}, email={user.email}")
        
        # 检查用户名是否已存在
        db_user = db.query(User).filter(User.username == user.username).first()
        if db_user:
            return response_error(code=400, msg="用户名已存在")
        
        # 检查邮箱是否已存在（如果提供了邮箱）
        if user.email:
            db_user = db.query(User).filter(User.email == user.email).first()
            if db_user:
                return response_error(code=400, msg="邮箱已存在")
        
        # 创建用户对象
        hashed_password = get_password_hash(user.password)
        
        # 使用安全的 User 对象创建方式
        user_data = {
            "username": user.username,
            "hashed_password": hashed_password,
        }
        
        # 只有当 email 不为 None 时才添加
        if user.email is not None:
            user_data["email"] = user.email
        
        new_user = User(**user_data)
        
        # 保存到数据库
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print(f"用户注册成功: {user.username}")
        return response_success(data={"msg": "注册成功", "user_id": new_user.id})
        
    except Exception as e:
        db.rollback()  # 回滚事务
        print(f"注册异常: {type(e).__name__}: {e}")
        traceback.print_exc()
        return response_error(code=500, msg=f"服务器内部错误: {str(e)[:100]}")


@router.get("/me", response_model=BaseResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    try:
        user_info = {
            "username": current_user.username,
            "email": getattr(current_user, 'email', None),
            "is_active": getattr(current_user, 'is_active', True),
            "created_at": getattr(current_user, 'created_at', None),
        }
        return response_success(data=user_info)
    except Exception as e:
        print(f"获取用户信息异常: {e}")
        return response_error(code=500, msg="获取用户信息失败")


@router.post("/forgot-password", response_model=BaseResponse)
def forgot_password(req: ForgotPasswordRequest, db: Session = Depends(get_db)) -> BaseResponse:
    """忘记密码"""
    try:
        if not req.email:
            return response_error(code=400, msg="请输入邮箱地址")
        
        user = db.query(User).filter(User.email == req.email).first()
        
        # 为了安全，无论用户是否存在都返回相同的信息
        if not user:
            print(f"邮箱不存在: {req.email}")
            return response_success(data={"msg": "如果邮箱存在，重置链接已发送"})
        
        # 生成重置令牌
        reset_token = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
        
        # 更新用户信息
        user.reset_token = reset_token
        user.reset_token_expires = expires_at
        db.add(user)
        db.commit()
        
        # 生成重置链接（在实际应用中应该发送邮件）
        reset_link = f"http://localhost:3000/reset-password?token={reset_token}"
        print(f"[密码重置] 用户: {user.username}, 重置链接: {reset_link}, 过期时间: {expires_at}")
        
        return response_success(data={"msg": "如果邮箱存在，重置链接已发送"})
        
    except Exception as e:
        db.rollback()
        print(f"忘记密码异常: {e}")
        return response_error(code=500, msg="服务器内部错误")


@router.post("/reset-password", response_model=BaseResponse)
def reset_password(req: ResetPasswordRequest, db: Session = Depends(get_db)) -> BaseResponse:
    """重置密码"""
    try:
        if not req.token or not req.new_password:
            return response_error(code=400, msg="令牌和新密码不能为空")
        
        if len(req.new_password) < 6:
            return response_error(code=400, msg="密码长度至少6位")
        
        now = datetime.now(timezone.utc)
        
        # 查找有效的重置令牌
        user = db.query(User).filter(
            User.reset_token == req.token,
            User.reset_token_expires.isnot(None),
            User.reset_token_expires > now
        ).first()
        
        if not user:
            return response_error(code=400, msg="无效或过期的重置令牌")
        
        # 更新密码
        hashed_password = get_password_hash(req.new_password)
        user.hashed_password = hashed_password
        user.reset_token = None
        user.reset_token_expires = None
        db.add(user)
        db.commit()
        
        print(f"密码重置成功: {user.username}")
        return response_success(data={"msg": "密码重置成功"})
        
    except Exception as e:
        db.rollback()
        print(f"重置密码异常: {e}")
        return response_error(code=500, msg="服务器内部错误")


@router.post("/change-password", response_model=BaseResponse)
def change_password(
    old_password: str,
    new_password: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> BaseResponse:
    """修改密码"""
    try:
        # 验证旧密码
        if not verify_password(old_password, current_user.hashed_password):
            return response_error(code=400, msg="旧密码错误")
        
        # 更新为新密码
        hashed_password = get_password_hash(new_password)
        current_user.hashed_password = hashed_password
        db.add(current_user)
        db.commit()
        
        return response_success(data={"msg": "密码修改成功"})
        
    except Exception as e:
        db.rollback()
        print(f"修改密码异常: {e}")
        return response_error(code=500, msg="服务器内部错误")


@router.get("/test", response_model=BaseResponse)
def test_connection(db: Session = Depends(get_db)):
    """测试数据库连接"""
    try:
        user_count = db.query(User).count()
        return response_success(data={
            "message": "数据库连接正常",
            "user_count": user_count
        })
    except Exception as e:
        print(f"数据库测试异常: {e}")
        traceback.print_exc()
        return response_error(code=500, msg=f"数据库连接失败: {str(e)}")