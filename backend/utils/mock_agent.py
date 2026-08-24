import random
import time
from datetime import datetime

from utils.influxdb_client import SingletonInfluxDBClient
from config import settings
from dotenv import load_dotenv

load_dotenv()

def generate_mock_metrics(
    url=settings.INFLUX_URL,
    token=settings.INFLUX_TOKEN,
    org=settings.INFLUX_ORG,
    bucket=settings.INFLUX_BUCKET,
    host=settings.HOST,
    interval=2,
    loops=100
):
    """
    随机生成监控数据,并写入InfluxDB，模拟服务器实时上报。
    参数:
        url, token, org, bucket: InfluxDB连接信息
        host: 模拟主机名称
        interval: 采样间隔（秒）
        loops: 上报次数（如None则无限循环）
    """
    influx_client = SingletonInfluxDBClient(url, token, org, bucket)
    for i in range(loops):
        cpu_usage = round(random.uniform(0, 100), 2)
        mem_usage = round(random.uniform(20, 80), 2)
        net_in = round(random.uniform(0, 200), 2)   # Mbps
        net_out = round(random.uniform(0, 200), 2)
        now = datetime.utcnow()
        influx_client.write_data(
            measurement="server_metrics",
            tags={"host": host},
            fields={
                "cpu_usage": cpu_usage,
                "mem_usage": mem_usage,
                "net_in": net_in,
                "net_out": net_out
            },
            timestamp=now
        )
        print(f"[{now.isoformat()}] host={host} cpu={cpu_usage}% mem={mem_usage}% net_in={net_in} net_out={net_out}")
        time.sleep(interval)
