<template>
  <div ref="chartRef" :style="{ width: '100%', height: chartHeight }"></div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount, computed } from 'vue'

// props
const props = defineProps({
  options: {
    type: Object,
    required: true,
  },
  height: {
    type: String,
    default: '400px',
  },
})

// dom ref and echarts instance
const chartRef = ref(null)
let chartInstance = null
const chartHeight = computed(() => props.height)

// lazy import echarts for better build split (optionally top import if needed, but per rules skip)
let echartsLib = null

function renderChart() {
  if (!chartRef.value || !echartsLib) return
  if (!chartInstance) {
    chartInstance = echartsLib.init(chartRef.value)
  }
  chartInstance.setOption(props.options, true)
}

function resizeChart() {
  if (chartInstance) {
    chartInstance.resize()
  }
}

function disposeChart() {
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
}

let resizeObserver = null

onMounted(async () => {
  if (typeof window !== 'undefined') {
    echartsLib = (await import('echarts')).default || (await import('echarts'))
    renderChart()
    window.addEventListener('resize', resizeChart)
    // more robust: observe container size changes for flex layouts
    if ('ResizeObserver' in window && chartRef.value) {
      resizeObserver = new ResizeObserver(() => resizeChart())
      resizeObserver.observe(chartRef.value)
    }
  }
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', resizeChart)
  if (resizeObserver && chartRef.value) {
    resizeObserver.unobserve(chartRef.value)
    resizeObserver = null
  }
  disposeChart()
})

watch(() => props.options, (newVal) => {
  if (chartInstance && newVal) {
    chartInstance.setOption(newVal, true)
  } else if (chartRef.value && echartsLib) {
    renderChart()
  }
}, { deep: true })

watch(() => props.height, () => {
  // just trigger a resize
  resizeChart()
})
</script>