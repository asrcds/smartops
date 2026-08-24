# celery_tasks.py
from celery import shared_task
from sqlalchemy.orm import Session
from utils.db import SessionLocal
from models.asset import Asset
from models.task import TaskRecord
import paramiko

@shared_task
def execute_ssh_task(asset_id: int, command: str, task_record_id: int):
    db = SessionLocal()
    try:
        # 1. 获取资产信息
        asset = db.query(Asset).filter(Asset.id == asset_id).first()
        if not asset:
            raise ValueError(f"Asset {asset_id} not found")
        
        # 2. 更新任务状态为 RUNNING（可选）
        task = db.query(TaskRecord).get(task_record_id)
        task.status = "RUNNING"
        db.commit()
        
        # 3. 执行 SSH 命令
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(
                asset.ip_address,
                port=asset.ssh_port or 22,
                username=asset.ssh_user,
                password=asset.ssh_password,
                timeout=10
            )
            stdin, stdout, stderr = ssh.exec_command(command)
            out = stdout.read().decode('utf-8')
            err = stderr.read().decode('utf-8')
            result = {"stdout": out, "stderr": err}
            
            # 4. 更新任务为成功
            task.status = "SUCCESS"
            task.result = result
        except Exception as e:
            task.status = "FAILED"
            task.result = {"error": str(e)}
        finally:
            ssh.close()
        
        db.commit()
    except Exception as e:
        db.rollback()
        # 可以重试或记录日志
        raise e
    finally:
        db.close()