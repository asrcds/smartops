<template>
  <div class="alert-page">
    <div class="alert-toolbar">
      <span class="toolbar-title">安全预警</span>
      <el-select v-model="selectedLevel" placeholder="筛选级别" class="level-filter" clearable @change="filterAlerts">
        <el-option v-for="item in levelOptions" :key="item.value" :label="item.label" :value="item.value"/>
      </el-select>
    </div>
    <el-table
      :data="filteredAlerts"
      style="width: 100%;"
      class="alert-table"
      height="540"
      :row-class-name="rowClassName"
      border>
      <el-table-column prop="time" label="时间" min-width="160"/>
      <el-table-column prop="level" label="级别" min-width="90">
        <template #default="{ row }">
          <el-tag :type="levelType(row.level)" disable-transitions>{{ row.level }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="host" label="主机" min-width="110"/>
      <el-table-column prop="content" label="内容" min-width="240"/>
    </el-table>
    <!-- 预留对接真实API的结构 -->
    <!--
    onMounted(() => {
      fetchAlerts();
    });

    function fetchAlerts() {
      // 调用后端API获取告警数据
    }
    -->
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// 模拟数据
const mockAlerts = [
  {
    time: '2024-06-01 16:32:21',
    level: '高',
    host: 'host-01',
    content: '检测到异常登录行为。',
  },
  {
    time: '2024-06-01 15:42:54',
    level: '中',
    host: 'host-03',
    content: 'CPU使用率持续超90%。',
  },
  {
    time: '2024-06-01 14:11:17',
    level: '低',
    host: 'host-02',
    content: '设备连接数超过阈值。',
  },
  {
    time: '2024-06-01 13:05:10',
    level: '高',
    host: 'host-02',
    content: '检测到可疑端口扫描活动。',
  },
  {
    time: '2024-06-01 09:23:44',
    level: '中',
    host: 'host-01',
    content: '短时内多次登录失败。',
  },
  {
    time: '2024-05-31 22:10:15',
    level: '低',
    host: 'host-04',
    content: '内存使用率达到80%。',
  }
]

const levelOptions = [
  { label: '高', value: '高' },
  { label: '中', value: '中' },
  { label: '低', value: '低' },
]

const selectedLevel = ref()

const alerts = ref(mockAlerts)

const filteredAlerts = computed(() => {
  if (!selectedLevel.value) return alerts.value
  return alerts.value.filter(item => item.level === selectedLevel.value)
})

function filterAlerts() {
  // 若后续联动接口可在此处理
}

function levelType(level) {
  if (level === '高') return 'danger'
  if (level === '中') return 'warning'
  if (level === '低') return 'info'
  return ''
}

function rowClassName({ row }) {
  switch (row.level) {
    case '高':
      return 'alert-row-high'
    case '中':
      return 'alert-row-mid'
    case '低':
      return 'alert-row-low'
    default:
      return ''
  }
}

// 预留对接后端的接口结构
// import { onMounted } from 'vue'
// function fetchAlerts() {
//   // API 调用逻辑
//   // alerts.value = await fetch('/api/alerts') ...
// }
// onMounted(() => {
//   // fetchAlerts()
// })
</script>

<style scoped>
.alert-page {
  padding: 32px 18px 0 18px;
  min-height: 90vh;
  background: linear-gradient(124deg, #f0f7fe 0%, #fafdff 100%);
}

.alert-toolbar {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
  gap: 16px;
}

.toolbar-title {
  font-size: 22px;
  font-weight: 700;
  color: #234;
  letter-spacing: 2px;
  margin-right: 32px;
}

.level-filter {
  width: 130px;
}

.alert-table {
  background: rgba(255,255,255,0.98);
  border-radius: 10px;
  box-shadow: 0 2px 10px #b0c8ee22;
  padding: 10px 0 0 0;
}

:deep(.el-tag.danger) {
  background-color: #fde2e1;
  border-color: #fde2e1;
  color: #e55454;
  font-weight: 600;
}
:deep(.el-tag.warning) {
  background-color: #fff5e2;
  border-color: #fff5e2;
  color: #e79a20;
  font-weight: 600;
}
:deep(.el-tag.info) {
  background-color: #ecf6fe;
  border-color: #ecf6fe;
  color: #238ae6;
  font-weight: 600;
}

.alert-row-high {
  background: #fff6f7;
}
.alert-row-mid {
  background: #fffbee;
}
.alert-row-low {
  background: #f0f7fe;
}

@media (max-width: 900px) {
  .alert-page {
    padding: 13px 2vw;
  }
}
</style>