from celery import Celery

celery_app = Celery(
    'backend_worker',
    broker='redis://localhost:6379/0',  # 可以根据需要调整 Redis 地址
    backend='redis://localhost:6379/1'  # 可选，任务结果存储
)

# 可选的自定义配置
celery_app.conf.task_serializer = 'json'
celery_app.conf.result_serializer = 'json'
celery_app.conf.accept_content = ['json']
celery_app.conf.timezone = 'Asia/Shanghai'
celery_app.conf.enable_utc = True