<template>
  <div class="dashboard-page">
    <!-- Top Bar -->
    <div class="dashboard-toolbar">
      <el-select v-model="selectedHost" placeholder="选择主机" style="width:180px;" @change="handleHostChange">
        <el-option
          v-for="host in hosts"
          :key="host.value"
          :label="host.label"
          :value="host.value"
        />
      </el-select>
      <el-select v-model="selectedRange" placeholder="时间范围" style="width:150px; margin-left:16px;" @change="handleRangeChange">
        <el-option v-for="range in timeRanges" :key="range.value" :label="range.label" :value="range.value" />
      </el-select>
      <el-checkbox v-model="autoRefresh" style="margin-left:16px;">10秒自动刷新</el-checkbox>
      <el-button icon="el-icon-refresh" @click="fetchAll" style="margin-left:16px;">刷新</el-button>
    </div>

    <!-- Card Section -->
    <div class="dashboard-cards">
      <el-card class="card-item asset-card">
        <div class="card-title">总资产数</div>
        <div class="card-value">{{ stats.assets }}</div>
      </el-card>
      <el-card class="card-item task-card">
        <div class="card-title">运行中任务</div>
        <div class="card-value">{{ stats.tasks }}</div>
      </el-card>
      <el-card class="card-item alert-card">
        <div class="card-title">告警数</div>
        <div class="card-value">{{ stats.alarms }}</div>
      </el-card>
    </div>

    <!-- Chart Section -->
    <div class="dashboard-charts">
      <div class="chart-box">
        <div class="chart-title">CPU 使用率 (%)</div>
        <!-- 修复：将 height 改为字符串 -->
        <Chart
          :options="cpuChartOptions"
          height="240"
          :theme="echartsTheme"
        />
      </div>
      <div class="chart-box">
        <div class="chart-title">内存使用率 (%)</div>
        <Chart
          :options="memChartOptions"
          height="240"
          :theme="echartsTheme"
        />
      </div>
      <div class="chart-box">
        <div class="chart-title">网络上行 (net_in)</div>
        <Chart
          :options="netInChartOptions"
          height="240"
          :theme="echartsTheme"
        />
      </div>
      <div class="chart-box">
        <div class="chart-title">网络下行 (net_out)</div>
        <Chart
          :options="netOutChartOptions"
          height="240"
          :theme="echartsTheme"
        />
      </div>
    </div>
    <div class="network-section">
      <NetworkChart :hosts="hostsForNetwork" />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onBeforeUnmount, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import Chart from '@/components/Chart.vue'
import NetworkChart from './Network.vue'

// Mock monitor API
const monitor = {
  async getHosts() {
    return [
      { label: '主机A', value: 'host_a' },
      { label: '主机B', value: 'host_b' },
      { label: '主机C', value: 'host_c' },
    ]
  },
  async getMetrics({ host, range }) {
    const now = Date.now()
    const step = {
      '1h': 60 * 1000,
      '6h': 6 * 60 * 1000,
      '24h': 24 * 60 * 1000
    }[range]
    const points = {
      '1h': 60, '6h': 60, '24h': 60
    }[range]
    const data = Array.from({ length: points }).map((_, idx) => {
      const t = now - (points - 1 - idx) * step
      return {
        timestamp: t,
        cpu: 20 + 20 * Math.random(),
        mem: 30 + 30 * Math.random(),
        net_in: 100 + 120 * Math.random(),
        net_out: 120 + 80 * Math.random()
      }
    })
    return data
  },
  async getStats() {
    return {
      assets: 34,
      tasks: 5,
      alarms: 2
    }
  }
}

// 主题适配
function detectTheme() {
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}
const echartsTheme = ref(detectTheme())
function handleThemeChange(e) {
  echartsTheme.value = e.matches ? 'dark' : 'light'
}
onMounted(() => {
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', handleThemeChange)
})
onBeforeUnmount(() => {
  window.matchMedia('(prefers-color-scheme: dark)').removeEventListener('change', handleThemeChange)
})

const timeRanges = [
  { label: '最近1小时', value: '1h' },
  { label: '最近6小时', value: '6h' },
  { label: '最近24小时', value: '24h' }
]

const hosts = ref([])
const selectedHost = ref('')
const selectedRange = ref('1h')
const autoRefresh = ref(false)
const stats = reactive({ assets: 0, tasks: 0, alarms: 0 })
const metricData = ref([])

// 加载主机列表 & 默认选中
async function fetchHosts() {
  const h = await monitor.getHosts()
  hosts.value = h
  if (h.length) selectedHost.value = h[0].value
}

// 加载监控指标
async function fetchMetrics() {
  if (!selectedHost.value) return
  const data = await monitor.getMetrics({ host: selectedHost.value, range: selectedRange.value })
  metricData.value = data
}

// 加载卡片区数据
async function fetchStats() {
  const s = await monitor.getStats()
  stats.assets = s.assets
  stats.tasks = s.tasks
  stats.alarms = s.alarms
}

async function fetchAll() {
  await Promise.all([fetchMetrics(), fetchStats()])
}

function handleHostChange() {
  fetchAll()
}
function handleRangeChange() {
  fetchAll()
}

let timer = null
watch(autoRefresh, val => {
  clearInterval(timer)
  if (val) {
    timer = setInterval(() => {
      fetchAll()
    }, 10000)
  }
})
onBeforeUnmount(() => {
  clearInterval(timer)
})

watch([selectedHost, selectedRange], () => {
  fetchAll()
})

// 初始化
onMounted(async () => {
  await fetchHosts()
  await fetchAll()
})

// 图表数据格式化
function formatTimestamps(data) {
  return data.map(d =>
    new Date(d.timestamp).toLocaleTimeString().replace(/^\d+:/, '')
  )
}
function getValues(data, key) {
  return data.map(d => Math.round(d[key]*100)/100)
}

const cpuChartOptions = computed(() => ({
  tooltip: { trigger: 'axis' },
  grid: { 
    left: 40, 
    right: 20, 
    top: 26, 
    bottom: 36,
    // 移除 containLabel 或设置为 false
    // containLabel: false
  },
  xAxis: {
    type: 'category',
    data: formatTimestamps(metricData.value),
    axisLabel: { color: 'inherit' }
  },
  yAxis: {
    type: 'value',
    axisLabel: { color: 'inherit', formatter: '{value} %' }
  },
  series: [{
    type: 'line',
    smooth: true,
    data: getValues(metricData.value, 'cpu'),
    name: 'CPU'
  }]
}))

const memChartOptions = computed(() => ({
  tooltip: { trigger: 'axis' },
  grid: { 
    left: 40, 
    right: 20, 
    top: 26, 
    bottom: 36
  },
  xAxis: {
    type: 'category',
    data: formatTimestamps(metricData.value),
    axisLabel: { color: 'inherit' }
  },
  yAxis: {
    type: 'value',
    axisLabel: { color: 'inherit', formatter: '{value} %' }
  },
  series: [{
    type: 'line',
    smooth: true,
    data: getValues(metricData.value, 'mem'),
    name: '内存'
  }]
}))

const netInChartOptions = computed(() => ({
  tooltip: { trigger: 'axis' },
  grid: { 
    left: 40, 
    right: 20, 
    top: 26, 
    bottom: 36
  },
  xAxis: {
    type: 'category',
    data: formatTimestamps(metricData.value),
    axisLabel: { color: 'inherit' }
  },
  yAxis: {
    type: 'value',
    axisLabel: { color: 'inherit', formatter: '{value}' }
  },
  series: [{
    type: 'line',
    areaStyle: {},
    smooth: true,
    data: getValues(metricData.value, 'net_in'),
    name: '上行'
  }]
}))

const netOutChartOptions = computed(() => ({
  tooltip: { trigger: 'axis' },
  grid: { 
    left: 40, 
    right: 20, 
    top: 26, 
    bottom: 36
  },
  xAxis: {
    type: 'category',
    data: formatTimestamps(metricData.value),
    axisLabel: { color: 'inherit' }
  },
  yAxis: {
    type: 'value',
    axisLabel: { color: 'inherit', formatter: '{value}' }
  },
  series: [{
    type: 'line',
    areaStyle: {},
    smooth: true,
    data: getValues(metricData.value, 'net_out'),
    name: '下行'
  }]
}))

const hostsForNetwork = computed(() => {
  return hosts.value.map(h => ({
    id: h.value,
    name: h.label
  }))
})
</script>

<style scoped>
.dashboard-page {
  min-height: 100vh;
  background: linear-gradient(120deg, #f1f6fc 0%, #e2eafe 100%);
  padding: 0 0 32px 0;
}
.dashboard-toolbar {
  display: flex;
  align-items: center;
  margin: 40px 0 28px 0;
  padding: 0 32px;
}
.dashboard-cards {
  display: flex;
  gap: 24px;
  margin: 0 32px 36px 32px;
}
.card-item {
  flex: 1;
  text-align: center;
  min-width: 150px;
  border-radius: 16px;
}
.card-title {
  font-size: 15px;
  color: #789;
  margin-bottom: 8px;
  letter-spacing: 0.5px;
}
.card-value {
  font-size: 32px;
  font-weight: 700;
  color: #234;
  margin-top: 4px;
}
.asset-card { border-bottom: 3px solid #59a9f7; }
.task-card { border-bottom: 3px solid #5bc77a;}
.alert-card { border-bottom: 3px solid #e55454;}
.dashboard-charts {
  display: grid;
  gap: 32px;
  grid-template-columns: repeat(2, 1fr);
  margin: 0 32px;
}
.chart-box {
  background: rgba(255,255,255,0.93);
  border-radius: 15px;
  padding: 14px 12px 6px 18px;
  box-shadow: 0 2px 6px #b0c8ee22;
  min-width: 0;
}
.chart-title {
  font-size: 16px;
  font-weight: bold;
  color: #234;
  margin-bottom: 8px;
  letter-spacing: 0.4px;
}
.network-section {
  margin: 32px 32px 0 32px;
}
@media (max-width: 800px) {
  .network-section {
    margin-left: 10px;
    margin-right: 10px;
  }
}
@media (max-width: 1200px) {
  .dashboard-charts {
    grid-template-columns: 1fr;
    gap: 24px;
  }
}
@media (max-width: 800px) {
  .dashboard-toolbar,
  .dashboard-cards,
  .dashboard-charts {
    margin-left: 10px;
    margin-right: 10px;
    padding: 0;
  }
}
</style>