from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List, Dict, Any
from datetime import datetime
from utils.influxdb_client import SingletonInfluxDBClient
from config import settings

router = APIRouter(prefix="/monitor", tags=["monitor"])

# 初始化 InfluxDB 客户端（使用配置）
influx_client = SingletonInfluxDBClient(
    url=settings.INFLUX_URL,
    token=settings.INFLUX_TOKEN,
    org=settings.INFLUX_ORG,
    bucket=settings.INFLUX_BUCKET
)

@router.get("/metrics")
def get_metrics(
    host: str = Query(..., description="主机名，例如 mock_server01"),
    measurement: str = Query("server_metrics", description="测量名称，默认 server_metrics"),
    fields: Optional[List[str]] = Query(None, description="要返回的字段列表，如 cpu_usage,mem_usage，不传则返回所有"),
    start: str = Query("-1h", description="开始时间，例如 -1h, -30m, 2024-01-01T00:00:00Z"),
    stop: str = Query("now()", description="结束时间，例如 now(), 2024-01-02T00:00:00Z"),
    window: Optional[str] = Query(None, description="聚合窗口，例如 1m, 5m，用于降采样")
):
    """
    查询指定主机的监控指标时序数据。
    返回格式适用于前端图表（如 ECharts）。
    """
    try:
        # 构建 Flux 查询
        flux_query = f'''
            from(bucket: "{influx_client.bucket}")
            |> range(start: {start}, stop: {stop})
            |> filter(fn: (r) => r._measurement == "{measurement}")
            |> filter(fn: (r) => r.host == "{host}")
        '''
        # 字段过滤
        if fields:
            field_filters = " or ".join([f'r._field == "{f}"' for f in fields])
            flux_query += f'|> filter(fn: (r) => {field_filters})'
        
        # 聚合窗口（降采样）
        if window:
            flux_query += f'''
                |> aggregateWindow(every: {window}, fn: mean, createEmpty: false)
            '''
        
        # 按时间排序
        flux_query += '|> sort(columns: ["_time"])'
        
        # 执行查询
        tables = influx_client.query_api.query(flux_query, org=influx_client.org)
        
        # 转换数据为前端友好格式：{ timestamps: [], series: { field1: [values], field2: [values] } }
        result = {"timestamps": [], "series": {}}
        for table in tables:
            for record in table.records:
                time_str = record.get_time().isoformat()
                field = record.get_field()
                value = record.get_value()
                if time_str not in result["timestamps"]:
                    result["timestamps"].append(time_str)
                if field not in result["series"]:
                    result["series"][field] = []
                # 对齐时间点：需要确保每个时间点都有所有字段的值，但 InfluxDB 返回的数据可能缺失。
                # 简化处理：直接追加，前端需要按时间对齐，或者改用表格格式。
                # 更可靠的方式：返回列表格式 [{time, field, value}]，由前端重构。
                # 这里返回原始列表，前端自行处理。
        
        # 改用更通用的格式：返回记录列表
        records = []
        for table in tables:
            for record in table.records:
                records.append({
                    "time": record.get_time().isoformat(),
                    "field": record.get_field(),
                    "value": record.get_value(),
                    "host": host
                })
        return {"code": 200, "msg": "success", "data": records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/hosts")
def get_hosts() -> List[str]:
    """
    获取当前有监控数据的所有主机列表（用于前端下拉选择）。
    """
    # 查询所有不重复的 host 标签值
    flux_query = f'''
        import "influxdata/influxdb/v1"
        v1.tagValues(bucket: "{influx_client.bucket}", tag: "host", predicate: (r) => r._measurement == "server_metrics")
    '''
    try:
        tables = influx_client.query_api.query(flux_query, org=influx_client.org)
        hosts = set()
        for table in tables:
            for record in table.records:
                hosts.add(record.get_value())
        return {"code": 200, "msg": "success", "data": sorted(list(hosts))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))