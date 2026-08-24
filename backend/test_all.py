from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime

from utils.db import SessionLocal, engine
from models.user import User
from models.asset import Asset
from models.task import TaskRecord
from utils.db import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def test_all():
    db: Session = SessionLocal()
    try:
        print("\n" + "="*30)
        print("🚀 开始综合业务逻辑测试")
        print("="*30)

        # ==========================================
        # 1. 用户模块测试
        # ==========================================
        print("\n[1/3] 测试用户模块 (User)...")

        
        test_username = "test_admin_crud"
        user = db.query(User).filter(User.username == test_username).first()
        if user:
            # 先删除资产
            db.query(Asset).filter(Asset.owner_id == user.id).delete()
            # 再删除任务
            db.query(TaskRecord).filter(TaskRecord.creator_id == user.id).delete()
            # 最后删除用户
            db.delete(user)
            db.commit()
            print("  ✅ 清理残留测试数据成功")
        else:
            user = User(
            username=test_username,
            email="test@example.com",
            hashed_password=pwd_context.hash("123456"),
            role="user"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            user_id = user.id
            print(f"  ✅ 创建用户成功: ID={user.id}, Name={user.username}")

            db_user = db.query(User).filter(User.username == test_username).first()
            assert db_user is not None, "用户查询失败"
            db_user.role = "admin"
            db.commit()
            print(f"  ✅ 查询并修改角色成功: Role={db_user.role}")

            user_id = db_user.id

        # ==========================================
        # 2. 资产模块测试
        # ==========================================
        print("\n[2/3] 测试资产模块 (Asset)...")
        asset_ip = "192.168.1.100"
        asset = Asset(
            asset_no="A001",
            ip_address=asset_ip,
            hostname="web-server-01",
            os_type="Ubuntu 22.04",
            status="在用",
            owner_id=user_id
        )
        db.add(asset)
        db.commit()
        db.refresh(asset)
        print(f"  ✅ 创建资产成功: IP={asset.ip_address}, Owner={asset.owner.username}")

        asset.status = "报废"
        db.commit()
        print(f"  ✅ 修改资产状态成功: Status={asset.status}")

        # 唯一性约束测试（IP 唯一性）
        try:
            dup_asset = Asset(
                asset_no="A002",
                ip_address=asset_ip,  # 重复 IP
                hostname="dup-server",
                os_type="CentOS",
                status="闲置",
                owner_id=user_id
            )
            db.add(dup_asset)
            db.commit()
            print("  ❌ 唯一性约束测试失败：允许了重复IP")
        except Exception as e:
            db.rollback()
            print(f"  ✅ 唯一性约束测试通过: 捕获到重复IP错误")
            # 重新开始事务（可选，因为后面还有 commit）
            # 但为了安全，可以重新创建会话，这里简单处理

        asset_id = asset.id

        # ==========================================
        # 3. 任务模块测试
        # ==========================================
        print("\n[3/3] 测试任务模块 (Task)...")
        task = TaskRecord(
            task_name="重启服务",
            command="systemctl restart nginx",
            target_hosts=["192.168.1.100", "192.168.1.101"],
            status="PENDING",
            creator_id=user_id
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        assert isinstance(task.target_hosts, list), "target_hosts 应该是列表"
        print(f"  ✅ 创建任务成功: Hosts={task.target_hosts}, Creator={task.creator.username}")

        task.status = "SUCCESS"
        task.result = "执行成功：nginx is running."
        # 使用 updated_at 而不是 finish_time
        task.updated_at = datetime.now()
        db.commit()
        print(f"  ✅ 更新任务状态成功: Status={task.status}")

        # ==========================================
        # 4. 清理数据 (Delete)
        # ==========================================
        print("[Cleanup] 清理测试数据...")
        test_user = db.query(User).filter(User.username == "test_admin_crud").first()
        if test_user:
            # 先删除关联的资产
            db.query(Asset).filter(Asset.owner_id == test_user.id).delete()
            # 可选：同时删除该用户创建的任务
            db.query(TaskRecord).filter(TaskRecord.creator_id == test_user.id).delete()
            # 确保删除操作先发送到数据库
            db.flush()
            # 再删除用户
            db.delete(test_user)
            db.commit()
            print(f"  ✅ 清理测试用户及其关联数据成功: {test_user.username}")
        else:
            print("  ⚠️ 未找到测试用户，跳过清理")
        
        print("\n" + "="*30)
        print("🎉 所有测试通过！系统运行正常。")
        print("="*30 + "\n")
    except Exception as e:
        db.rollback()
        print(f"\n❌ 测试过程中发生错误: {e}")
        raise e
    finally:
        db.close()
if __name__ == "__main__":
    test_all()