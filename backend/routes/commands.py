from fastapi import APIRouter, HTTPException, Query, Depends, BackgroundTasks
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from utils.db import get_db
from models.task import TaskRecord
from models.asset import Asset
from models.user import User
from routes.auth import get_current_user
from utils.response import response_success, BaseResponse
import random
import time
from utils.db import SessionLocal

router = APIRouter()

class ExecuteCommandRequest(BaseModel):
    command: str
    target_asset_ids: List[int]

class TaskRecordBase(BaseModel):
    id: int
    asset_id: int
    command: str
    status: str
    result: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

# 模拟命令执行的后台任务
def simulate_execute(asset_id: int, command: str, task_record_id: int):
    db = SessionLocal()
    try:
        # 更新状态为 RUNNING
        task = db.query(TaskRecord).filter(TaskRecord.id == task_record_id).first()
        if not task:
            return
        task.status = "RUNNING"
        db.commit()

        # 模拟执行延迟（1~5 秒）
        delay = random.uniform(1, 5)
        time.sleep(delay)

        # 90% 成功，10% 失败
        if random.random() < 0.9:
            # 根据命令内容生成动态模拟输出
            stdout = generate_mock_output(command, asset_id)
            stderr = ""
            task.status = "SUCCESS"
            task.result = {"stdout": stdout, "stderr": stderr}
        else:
            task.status = "FAILED"
            task.result = {"error": f"模拟错误：命令 '{command}' 执行失败（随机失败）"}

        db.commit()
    except Exception as e:
        task.status = "FAILED"
        task.result = {"error": str(e)}
        db.commit()
    finally:
        db.close()

def generate_mock_output(command: str, asset_id: int) -> str:
    """根据命令类型和资产 ID 生成动态模拟输出"""
    cmd_lower = command.lower()
    if "ls" in cmd_lower:
        return "file1.txt\nfile2.py\nconfig.json\nmock_data.bin"
    elif "df" in cmd_lower:
        return "Filesystem     1K-blocks    Used Available Use% Mounted on\n/dev/sda1       10240000 5123456   5116544  50% /\ntmpfs           1024000       0   1024000   0% /dev/shm"
    elif "top" in cmd_lower:
        return f"top - {time.ctime()}  up 1 day,  load average: {random.uniform(0, 5):.2f}, {random.uniform(0, 5):.2f}, {random.uniform(0, 5):.2f}\nTasks: {random.randint(80, 200)} total,   1 running,  {random.randint(70, 190)} sleeping,   0 stopped,   0 zombie"
    elif "ping" in cmd_lower:
        return f"PING {command.split()[-1]} 56(84) bytes of data.\n64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time={random.uniform(0.1, 10):.2f} ms"
    else:
        return f"模拟命令 '{command}' 执行成功 (asset_id={asset_id})\n生成时间: {time.ctime()}\n随机数: {random.randint(1, 100)}"

@router.post("/execute", response_model=BaseResponse)
def execute_command(
    req: ExecuteCommandRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    submitted_task_ids = []
    for asset_id in req.target_asset_ids:
        asset = db.query(Asset).filter(Asset.id == asset_id).first()
        if not asset:
            raise HTTPException(status_code=404, detail=f"Asset {asset_id} not found")

        task_record = TaskRecord(
            task_name=f"执行命令: {req.command}",
            command=req.command,
            target_hosts=[asset.ip_address],
            status="PENDING",
            creator_id=current_user.id
        )
        db.add(task_record)
        db.commit()
        db.refresh(task_record)

        background_tasks.add_task(simulate_execute, asset_id, req.command, task_record.id)
        submitted_task_ids.append(task_record.id)

    return response_success(data={"message": "任务已提交", "submitted_task_ids": submitted_task_ids})

@router.get("/history", response_model=BaseResponse)
def get_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)   # 可选，只返回当前用户的任务
):
    query = db.query(TaskRecord).filter(TaskRecord.creator_id == current_user.id)
    total = query.count()
    records = (
        query.order_by(desc(TaskRecord.created_at))
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    data = {
        "total": total,
        "page": page,
        "page_size": page_size,
        "records": [TaskRecordBase.model_validate(rec) for rec in records]
    }
    return response_success(data=data)

@router.get("/result/{task_id}", response_model=BaseResponse)
def get_result(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = db.query(TaskRecord).filter(TaskRecord.id == task_id, TaskRecord.creator_id == current_user.id).first()
    if not record:
        raise HTTPException(status_code=404, detail="任务未找到或无权限")
    data = {
        "status": record.status,
        "result": record.result if record.status in ["SUCCESS", "FAILED"] else None
    }
    return response_success(data=data)