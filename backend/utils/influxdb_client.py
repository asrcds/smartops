from threading import Lock
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from typing import List, Dict, Any

class SingletonInfluxDBClient:
    _instance = None
    _lock = Lock()

    def __new__(cls, url: str, token: str, org: str, bucket: str):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(SingletonInfluxDBClient, cls).__new__(cls)
                    cls._instance._init_client(url, token, org, bucket)
        return cls._instance

    def _init_client(self, url: str, token: str, org: str, bucket: str):
        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()
        self.bucket = bucket
        self.org = org

    def write_data(self, measurement: str, tags: Dict[str, str], fields: Dict[str, Any], timestamp=None):
        """
        写入一条监控数据（如CPU、内存、网络等），measurement为指标名。
        :param measurement: 指标，如 "cpu"
        :param tags: 标签，比如 {"host": "server01"}
        :param fields: 字段，比如 {"usage_idle": 90.0, "usage_user": 5.0}
        :param timestamp: 时间戳，可选，标准时间或毫秒/纳秒
        """
        point = Point(measurement)
        for k, v in tags.items():
            point = point.tag(k, v)
        for k, v in fields.items():
            point = point.field(k, v)
        if timestamp:
            point = point.time(timestamp)
        self.write_api.write(bucket=self.bucket, org=self.org, record=point)

    def query_data(self, measurement: str, tags: Dict[str, str] = None,
                   start: str = "-1h", stop: str = "now()") -> List[Dict]:
        """
        查询某指标数据，支持时间段和标签筛选。
        :param measurement: 指标名
        :param tags: 过滤标签
        :param start: 开始时间，如 "-1h"，"2024-01-01T00:00:00Z"
        :param stop: 结束时间，如 "now()"
        :return: [{time, field1, field2, ...}]
        """
        tag_filter = " and ".join([f'r["{k}"] == "{v}"' for k, v in (tags or {}).items()])
        filter_exp = f'|> filter(fn: (r) => r._measurement == "{measurement}"' + (f' and {tag_filter}' if tag_filter else '') + ')'

        flux_query = f'''
            from(bucket: "{self.bucket}")
            |> range(start: {start}, stop: {stop})
            {filter_exp}
        '''
        tables = self.query_api.query(flux_query, org=self.org)
        # 结果转换为前端绘图友好结构
        result = []
        for table in tables:
            for record in table.records:
                item = {
                    "time": str(record.get_time()),
                    "field": record.get_field(),
                    "value": record.get_value()
                }
                # 保留tags信息
                for tag_k, tag_v in (tags or {}).items():
                    item[tag_k] = tag_v
                result.append(item)
        return result

# 用法示例（建议实际环境里用配置文件载入连接参数）
# client = SingletonInfluxDBClient(url="http://localhost:8086", token="your_token", org="your_org", bucket="your_bucket")
# client.write_data("cpu", {"host": "server01"}, {"usage_idle": 80, "usage_user": 10})
# data = client.query_data("cpu", tags={"host": "server01"}, start="-24h")