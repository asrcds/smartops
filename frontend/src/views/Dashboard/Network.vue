<template>
  <div class="network-chart-box">
    <div class="chart-header">
      <span class="chart-title">网络流量趋势</span>
      <el-date-picker
        v-model="range"
        type="datetimerange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        :shortcuts="shortcuts"
        size="small"
        @change="handleRangeChange"
      />
      <el-select
        v-model="selectedHosts"
        multiple
        filterable
        clearable
        placeholder="选择主机"
        size="small"
        class="host-select"
        @change="fetchData"
      >
        <el-option
          v-for="item in hosts"
          :key="item.id || item"
          :label="item.name || item"
          :value="item.id || item"
        />
      </el-select>
    </div>
    <div>
      <!-- 注意：这里使用 VChart，不是 ECharts -->
      <VChart
        :option="chartOption"
        autoresize
        style="height:320px;"
        v-loading="loading"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, defineProps } from 'vue'
import { ElMessage } from 'element-plus'

// 1. 导入 vue-echarts（关键修复）
import VChart from 'vue-echarts'

// 2. 导入 echarts 核心并注册组件
import { use } from 'echarts/core'
import { LineChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  DataZoomComponent,
  TitleComponent
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { UniversalTransition } from 'echarts/features'

// 3. 注册必须的组件
use([
  LineChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  DataZoomComponent,
  TitleComponent,
  CanvasRenderer,
  UniversalTransition
])

// 4. 定义 props
const props = defineProps({
  hosts: {
    type: Array,
    required: true,
    default: () => []
  }
})

// 向父组件暴露方法或数据，若有需要
// defineExpose({})

const range = ref([])
const shortcuts = [
  {
    text: '最近1小时',
    value: () => [new Date(Date.now() - 3600 * 1000), new Date()]
  },
  {
    text: '最近6小时',
    value: () => [new Date(Date.now() - 6 * 3600 * 1000), new Date()]
  },
  {
    text: '今天',
    value: () => {
      const start = new Date()
      start.setHours(0, 0, 0, 0)
      return [start, new Date()]
    }
  }
]

const selectedHosts = ref([])
const loading = ref(false)
const chartData = ref([]) // [{ host, timestamps: [x], up: [y1], down: [y2] }, ...]

function defaultHosts() {
  // 默认选全部主机
  if (Array.isArray(props.hosts) && props.hosts.length > 0) {
    return props.hosts.map(h => h.id || h)
  }
  return []
}

watch(
  () => props.hosts,
  (val) => {
    selectedHosts.value = defaultHosts()
    fetchData()
  },
  { immediate: true }
)

watch(
  () => range.value,
  () => {
    fetchData()
  }
)

watch(selectedHosts, fetchData)

// 格式化系列，用于画双折线
const chartOption = computed(() => {
  if (!chartData.value.length) {
    return {
      title: { 
        text: '暂无数据', 
        left: 'center', 
        textStyle: { 
          color: '#bbb', 
          fontWeight: 400 
        } 
      }
    }
  }
  
  let series = []
  let legend = []
  
  chartData.value.forEach(hostData => {
    legend.push(`${hostData.hostName} 上行`)
    legend.push(`${hostData.hostName} 下行`)
    
    series.push(
      {
        name: `${hostData.hostName} 上行`,
        type: 'line',
        yAxisIndex: 0,
        data: hostData.up,
        smooth: true,
        symbol: 'circle',
        lineStyle: {
          width: 2
        },
        itemStyle: {
          color: '#409eff'
        }
      },
      {
        name: `${hostData.hostName} 下行`,
        type: 'line',
        yAxisIndex: 1,
        data: hostData.down,
        smooth: true,
        symbol: 'rect',
        lineStyle: {
          width: 2
        },
        itemStyle: {
          color: '#67c23a'
        }
      }
    )
  })

  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { 
        type: 'cross',
        label: {
          backgroundColor: '#6a7985'
        }
      }
    },
    legend: { 
      data: legend,
      top: 10
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '12%',
      top: '20%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: chartData.value[0]?.timestamps || [],
      axisLabel: { 
        formatter: (value) => {
          if (!value) return ''
          return value.replace('T', '\n')
        }
      }
    },
    yAxis: [
      {
        type: 'value',
        name: '上行流量 (Mbps)',
        min: 0,
        position: 'left',
        axisLine: {
          show: true
        }
      },
      {
        type: 'value',
        name: '下行流量 (Mbps)',
        min: 0,
        position: 'right',
        axisLine: {
          show: true
        }
      }
    ],
    dataZoom: [
      { 
        type: 'slider', 
        xAxisIndex: 0, 
        height: 12, 
        bottom: 8, 
        showDetail: false 
      }
    ],
    series
  }
})

// 获取数据
async function fetchData() {
  if (!selectedHosts.value.length) {
    chartData.value = []
    return
  }
  loading.value = true
  try {
    // 模拟数据，实际中替换为你的 API
    const mockData = [
      {
        host: '1',
        hostName: '服务器1',
        timestamps: ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00'],
        up: [120, 132, 101, 134, 90, 230, 210],
        down: [220, 182, 191, 234, 290, 330, 310]
      },
      {
        host: '2',
        hostName: '服务器2',
        timestamps: ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00'],
        up: [150, 232, 201, 154, 190, 330, 410],
        down: [320, 332, 301, 334, 390, 330, 320]
      }
    ]
    
    chartData.value = mockData
    
  } catch (e) {
    console.error('获取网络监控数据失败:', e)
    chartData.value = []
    ElMessage.error('获取网络监控数据失败')
  } finally {
    loading.value = false
  }
}

function handleRangeChange() {
  fetchData()
}
</script>

<style scoped>
.network-chart-box {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 14px;
  box-shadow: 0 2px 10px rgba(0, 24, 128, 0.1);
  padding: 16px 20px 10px 20px;
  min-width: 0;
  margin-bottom: 16px;
}
.chart-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}
.chart-title {
  font-size: 16px;
  font-weight: 600;
  color: #234;
  letter-spacing: 0.4px;
  margin-right: 12px;
}
.host-select {
  max-width: 290px;
  min-width: 120px;
  flex: 1;
}
</style>