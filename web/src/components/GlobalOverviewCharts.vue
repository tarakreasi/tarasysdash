<template>
  <div class="grid grid-cols-1 xl:grid-cols-2 gap-6 mb-6">
    <!-- CPU Chart -->
    <div class="flex flex-col gap-4 rounded-xl bg-surface-dark/60 backdrop-blur-sm p-6 border border-border-color shadow-lg hover:shadow-[0_0_15px_rgba(37,209,244,0.15)] transition-all">
      <div class="flex justify-between items-center">
        <div>
          <p class="text-slate-400 text-sm font-medium uppercase tracking-wider">System CPU Load (Avg)</p>
          <p class="text-white text-2xl font-bold mt-1">{{ cpuLoad }}% <span class="text-sm font-normal text-slate-500">REAL-TIME</span></p>
        </div>
        <div class="flex gap-2">
          <span class="w-3 h-3 rounded-full bg-primary shadow-[0_0_8px_#25d1f4]"></span>
          <span class="text-xs text-slate-400">Cluster</span>
        </div>
      </div>
      <div id="cpu-chart" class="relative h-[200px] w-full"></div>
    </div>
    
    <!-- Memory Chart -->
    <div class="flex flex-col gap-4 rounded-xl bg-surface-dark/60 backdrop-blur-sm p-6 border border-border-color shadow-lg hover:shadow-[0_0_15px_rgba(168,85,247,0.15)] transition-all">
      <div class="flex justify-between items-center">
        <div>
          <p class="text-slate-400 text-sm font-medium uppercase tracking-wider">Cluster Memory Usage</p>
          <p class="text-white text-2xl font-bold mt-1">{{ memoryGB }} <span class="text-sm font-normal text-slate-500">GB</span></p>
        </div>
        <div class="flex gap-2">
          <span class="w-3 h-3 rounded-full bg-purple-500 shadow-[0_0_8px_#a855f7]"></span>
          <span class="text-xs text-slate-400">RAM</span>
        </div>
      </div>
      <div id="memory-chart" class="relative h-[200px] w-full"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, nextTick, watch } from 'vue'
import * as echarts from 'echarts/core'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

echarts.use([LineChart, GridComponent, TooltipComponent, CanvasRenderer])

const props = defineProps<{
  cpuLoad: number
  memoryGB: number
  history: Array<{ timestamp: number, avg_cpu: number, avg_memory: number }>
}>()

let cpuChart: echarts.ECharts | null = null
let memoryChart: echarts.ECharts | null = null

// --- Chart Rendering ---
function renderCpuChart() {
  const dom = document.getElementById('cpu-chart')
  if (!dom) return
  if (!cpuChart) cpuChart = echarts.init(dom)
  
  const option = {
    grid: { left: 0, right: 0, top: 10, bottom: 0 },
    xAxis: { type: 'category', show: false },
    yAxis: { type: 'value', show: false, min: 0, max: 100 },
    tooltip: { trigger: 'axis', formatter: '{b}<br />{c}%' },
    series: [{
      data: [],
      type: 'line',
      smooth: true,
      showSymbol: false,
      lineStyle: { color: '#25d1f4', width: 2 },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(37, 209, 244, 0.4)' },
          { offset: 1, color: 'rgba(37, 209, 244, 0.0)' }
        ])
      }
    }]
  }
  cpuChart.setOption(option)
}

function updateCpuChart(metrics: any[]) {
    if (!cpuChart) return
    const data = metrics.map(m => m.avg_cpu.toFixed(1))
    const labels = metrics.map(m => new Date(m.timestamp * 1000).toLocaleTimeString())
    
    cpuChart.setOption({
        xAxis: { data: labels },
        series: [{ data: data }]
    })
}

function renderMemoryChart() {
   const dom = document.getElementById('memory-chart')
   if (!dom) return
   if (!memoryChart) memoryChart = echarts.init(dom)

   const option = {
    grid: { left: 0, right: 0, top: 10, bottom: 0 },
    xAxis: { type: 'category', show: false },
    yAxis: { type: 'value', show: false, min: 0 },
    tooltip: { trigger: 'axis', formatter: '{b}<br />{c} GB' },
    series: [{
      data: [],
      type: 'line',
      smooth: true,
      showSymbol: false,
      lineStyle: { color: '#a855f7', width: 2 },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(168, 85, 247, 0.4)' },
          { offset: 1, color: 'rgba(168, 85, 247, 0.0)' }
        ])
      }
    }]
  }
  memoryChart.setOption(option)
}

function updateMemoryChart(metrics: any[]) {
    if (!memoryChart) return
    const data = metrics.map(m => (m.avg_memory / 1073741824).toFixed(2))
    const labels = metrics.map(m => new Date(m.timestamp * 1000).toLocaleTimeString())

    memoryChart.setOption({
        xAxis: { data: labels },
        series: [{ data: data }]
    })
}

function handleResize() {
  cpuChart?.resize()
  memoryChart?.resize()
}

// Watch props.history
watch(() => props.history, (newMetrics) => {
  if (newMetrics && newMetrics.length > 0) {
    const chartData = [...newMetrics].reverse()
    updateCpuChart(chartData)
    updateMemoryChart(chartData)
  } else {
    updateCpuChart([])
    updateMemoryChart([])
  }
}, { deep: true })

onMounted(() => {
  nextTick(() => {
     renderCpuChart()
     renderMemoryChart()
     // Initial render with current data if any
     if (props.history && props.history.length > 0) {
         const chartData = [...props.history].reverse()
         updateCpuChart(chartData)
         updateMemoryChart(chartData)
     }
  })
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  cpuChart?.dispose()
  memoryChart?.dispose()
})
</script>
