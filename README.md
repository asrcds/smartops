# SmartOps — 智能运维监控系统

> 面向 IT 运维的轻量级监控与任务执行平台。集中管理服务器资产、实时监控系统指标、批量下发运维命令。


## 📌 项目定位

本系统解决运维工作中的两个核心痛点：

- **集中管理**：统一管理多台服务器的资产信息（IP、主机名、操作系统、状态等）
- **批量操作**：向多台服务器批量下发 Shell 命令，并追踪执行结果

系统采用前后端分离架构，后端提供 RESTful API，前端提供可视化操作界面。监控数据存储于时序数据库，支持历史趋势查询与图表展示。


## 🛠 技术栈

| 层级 | 技术选型 |
| :--- | :--- |
| **后端框架** | FastAPI (Python 3.9+) |
| **前端框架** | Vue 3 + Vite |
| **UI 组件库** | Element Plus |
| **关系型数据库** | MySQL (SQLAlchemy ORM) |
| **时序数据库** | InfluxDB 2.x |
| **任务队列** | Celery + Redis |
| **可视化** | ECharts |
| **认证** | JWT (python-jose) |
| **SSH 客户端** | Paramiko |


## 📁 系统架构



## 🚀 核心功能

### 后端模块

| 模块 | 功能 |
| :--- | :--- |
| **用户认证** | 注册 / 登录 / JWT 令牌 / 密码重置 |
| **资产管理** | 服务器资产的增删改查（IP、主机名、OS、状态） |
| **命令执行** | 向指定资产下发 Shell 命令，支持批量执行 |
| **任务队列** | 通过 Celery 异步执行耗时命令，避免阻塞 |
| **监控数据** | 查询 InfluxDB 中的 CPU/内存/网络时序数据 |
| **数据模拟** | 自动生成模拟监控数据，便于功能演示 |

### 前端页面

| 页面 | 功能 |
| :--- | :--- |
| **登录/注册** | 用户身份认证与账号注册 |
| **仪表盘** | CPU/内存/网络流量实时趋势图，支持主机切换与时间范围筛选 |
| **资产管理** | 资产列表展示、搜索、状态修改、删除 |
| **命令下发** | 选择目标资产 → 输入 Shell 命令 → 批量执行 → 查看结果 |
| **任务列表** | 查看历史命令执行记录与状态（等待/执行中/成功/失败） |
| **用户管理** | 管理员查看用户列表、修改角色、删除用户 |
| **密码修改** | 当前用户修改密码 |


## 🔧 快速启动

### 环境要求
- Python 3.9+
- Node.js 16+
- MySQL 5.7+
- InfluxDB 2.x
- Redis（可选，Celery 依赖）

### 1. 克隆项目

git clone https://github.com/asrcds/smartops.git
cd smartops


### 2. 后端启动和配置
```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量（创建 .env 文件）
# 参考下方配置说明

# 初始化数据库表
python -c "from utils.db import engine; from models import *; Base.metadata.create_all(engine)"

# 启动后端服务
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
### 3.前端配置与启动
```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```
访问 http://localhost:5173 进入前端页面。
### 4.启动模拟数据写入
```bash
# 在 backend 目录下运行
python mock_data_writer.py
```
### 5.启动 Celery 任务队列
```bash
# 在 backend 目录下运行
celery -A celery_worker worker --loglevel=info
```
## ⚙️ 环境变量配置
```bash
# MySQL
DB_URL=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=smartops

# InfluxDB
INFLUX_URL=http://localhost:8086
INFLUX_TOKEN=your_influxdb_token
INFLUX_ORG=your_org
INFLUX_BUCKET=your_bucket

# JWT
SECRET_KEY=your_jwt_secret_key

# 模拟数据主机名
HOST=mock_server01
```
## 📄 后续研究方向
本系统是本科毕业设计作品，后续将在硕士课题中进一步演进：

日志数据接入：采集系统日志与调用链数据，替代纯指标监控

图结构分析：将调用链关系抽象为拓扑图，辅助故障定位

多智能体诊断：基于 LLM 构建导航员/诊断员/验证员协作系统，实现自动化根因分析

智能运维闭环：从“展示数据”升级为“自动发现问题 → 定位根因 → 建议修复方案”
## 📝 License
仅供学习研究使用。


