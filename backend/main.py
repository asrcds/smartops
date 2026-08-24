from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, assets, users, monitor, commands
from models.asset import Asset
from sqlalchemy import inspect
from utils.db import engine
app = FastAPI(title="智能运维监控系统")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 检查实际列
inspector = inspect(engine)
print([c['name'] for c in inspector.get_columns('assets')])
# 如果输出包含 'ssh_port'，则数据库正常

# 清除模型元数据缓存
from sqlalchemy import MetaData
Asset.metadata.clear()
# 重新加载
Asset.__table__.create(engine, checkfirst=True)

@app.on_event("startup")
def init_test_users():
    from utils.db import SessionLocal
    from models.user import User
    from passlib.context import CryptContext
    db = SessionLocal()
    pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not db.query(User).filter(User.username == "user1").first():
        db.add(User(
            username="user1",
            hashed_password=pwd.hash("test123"),
            role="user",
            email="user1@test.com",
            is_active=True
        ))
        db.commit()
        print("测试用户 user1 创建成功")
    db.close()
@app.get("/")
async def root():
    return {"message": "Welcome to SmartOps API"}

# 注册路由
app.include_router(auth.router)
app.include_router(assets.router, prefix="/assets")
app.include_router(users.router)
app.include_router(monitor.router, prefix="/monitor")
app.include_router(commands.router, prefix="/commands")
# 如果你坚持要自动创建测试用户，请使用以下方式（确保字段名正确，且使用已有的 engine）
# 但更推荐在单独的脚本中执行一次，而不是放在 startup 事件中。