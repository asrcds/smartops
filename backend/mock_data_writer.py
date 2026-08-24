from utils.mock_agent import generate_mock_metrics
from config import settings


if __name__ == "__main__":
    generate_mock_metrics(
        url=settings.INFLUX_URL,
        token=settings.INFLUX_TOKEN,
        org=settings.INFLUX_ORG,
        bucket=settings.INFLUX_BUCKET,
        host=settings.HOST,
        interval=2,
        loops=100   # 或设置为 None 无限循环
    )