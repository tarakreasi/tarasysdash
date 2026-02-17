<template>
  <div class="grid grid-cols-1 xl:grid-cols-3 gap-6 mb-6">
    <!-- CPU Chart -->
    <div class="flex flex-col gap-4 rounded-xl bg-surface-dark/60 backdrop-blur-sm p-6 border border-border-color shadow-lg hover:shadow-[0_0_15px_rgba(37,209,244,0.15)] transition-all">
      <div class="flex justify-between items-center">
        <div>
          <p class="text-slate-400 text-sm font-medium uppercase tracking-wider">System CPU Load (Avg)</p>
          <p class="text-white text-2xl font-bold mt-1">{{ cpuLoad }}% <span class="text-sm font-normal text-slate-500">REAL-TIME</span></p>
        </div>
        <div class="flex gap-2">
          <span class="w-3 h-3 rounded-full bg-primary shadow-[0_0_8px_#25d1f4]"></span>
          <span class="text-xs text-slate-400">Cluster Avg</span>
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
          <span class="text-xs text-slate-400">Cluster Total</span>
        </div>
      </div>
      <div id="memory-chart" class="relative h-[200px] w-full"></div>
    </div>

    <!-- Network Traffic Chart -->
    <div class="flex flex-col gap-4 rounded-xl bg-surface-dark/60 backdrop-blur-sm p-6 border border-border-color shadow-lg hover:shadow-[0_0_15px_rgba(74,222,128,0.15)] transition-all">
      <div class="flex justify-between items-center">
        <div>
          <p class="text-slate-400 text-sm font-medium uppercase tracking-wider">Cluster Network Traffic</p>
          <p class="text-white text-2xl font-bold mt-1">Mbps <span class="text-sm font-normal text-slate-500">HISTORY</span></p>
        </div>
        <div class="flex flex-col gap-1 items-end">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-green-400"></span>
            <span class="text-[10px] text-slate-400">Inbound</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-blue-400"></span>
            <span class="text-[10px] text-slate-400">Outbound</span>
          </div>
        </div>
      </div>
      <div id="network-chart" class="relative h-[200px] w-full"></div>
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
  history: Array<{ timestamp: number, avg_cpu: number, avg_memory: number, avg_net_in: number, avg_net_out: number }>
}>()

let cpuChart: echarts.ECharts | null = null
let memoryChart: echarts.ECharts | null = null
let networkChart: echarts.ECharts | null = null

// --- Chart Rendering ---
function renderCpuChart() {
  const dom = document.getElementById('cpu-chart')
  if (!dom) return
  if (!cpuChart) cpuChart = echarts.init(dom)
  
  const option = {
    grid: { left: 40, right: 10, top: 10, bottom: 20 },
    xAxis: { 
        type: 'category', 
        show: true,
        axisLabel: { color: '#64748b', fontSize: 10 },
        axisLine: { show: false },
        axisTick: { show: false }
    },
    yAxis: { type: 'value', show: false, min: 0, max: 100 },
    tooltip: { 
        trigger: 'axis', 
        backgroundColor: 'rgba(15, 23, 42, 0.9)',
        borderColor: '#1e293b',
        textStyle: { color: '#f8fafc' },
        formatter: (params: any) => {
            const p = params[0]
            return `<div class="font-sans">
                      <div class="text-slate-400 text-[10px] uppercase mb-1">${p.name}</div>
                      <div class="flex items-center gap-2">
                        <span class="w-2 h-2 rounded-full bg-primary"></span>
                        <span class="font-bold">${p.value}%</span>
                      </div>
                    </div>`
        }
    },
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
    const labels = metrics.map(m => {
        const d = new Date(m.timestamp * 1000)
        return d.getHours().toString().padStart(2, '0') + ':' + d.getMinutes().toString().padStart(2, '0') + ':' + d.getSeconds().toString().padStart(2, '0')
    })
    
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
    grid: { left: 40, right: 10, top: 10, bottom: 20 },
    xAxis: { 
        type: 'category', 
        show: true,
        axisLabel: { color: '#64748b', fontSize: 10 },
        axisLine: { show: false },
        axisTick: { show: false }
    },
    yAxis: { type: 'value', show: false, min: 0 },
    tooltip: { 
        trigger: 'axis', 
        backgroundColor: 'rgba(15, 23, 42, 0.9)',
        borderColor: '#1e293b',
        textStyle: { color: '#f8fafc' },
        formatter: (params: any) => {
            const p = params[0]
            return `<div class="font-sans">
                      <div class="text-slate-400 text-[10px] uppercase mb-1">${p.name}</div>
                      <div class="flex items-center gap-2">
                        <span class="w-2 h-2 rounded-full bg-purple-500"></span>
                        <span class="font-bold">${p.value} GB</span>
                      </div>
                    </div>`
        }
    },
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
    const labels = metrics.map(m => {
        const d = new Date(m.timestamp * 1000)
        return d.getHours().toString().padStart(2, '0') + ':' + d.getMinutes().toString().padStart(2, '0') + ':' + d.getSeconds().toString().padStart(2, '0')
    })

    memoryChart.setOption({
        xAxis: { data: labels },
        series: [{ data: data }]
    })
}

function renderNetworkChart() {
   const dom = document.getElementById('network-chart')
   if (!dom) return
   if (!networkChart) networkChart = echarts.init(dom)

   const option = {
    grid: { left: 40, right: 10, top: 10, bottom: 20 },
    xAxis: { 
        type: 'category', 
        show: true,
        axisLabel: { color: '#64748b', fontSize: 10 },
        axisLine: { show: false },
        axisTick: { show: false }
    },
    yAxis: { type: 'value', show: false, min: 0 },
    tooltip: { 
        trigger: 'axis', 
        backgroundColor: 'rgba(15, 23, 42, 0.9)',
        borderColor: '#1e293b',
        textStyle: { color: '#f8fafc' },
        formatter: (params: any) => {
            return `<div class="font-sans">
                      <div class="text-slate-400 text-[10px] uppercase mb-1">${params[0].name}</div>
                      ${params.map((p:any) => `
                        <div class="flex items-center gap-2 mb-0.5">
                            <span class="w-2 h-2 rounded-full" style="background-color: ${p.color}"></span>
                            <span class="text-xs">${p.seriesName}:</span>
                            <span class="font-bold ml-auto">${p.value} Mbps</span>
                        </div>
                      `).join('')}
                    </div>`
        }
    },
    series: [
        {
            name: 'Inbound',
            data: [],
            type: 'line',
            smooth: true,
            showSymbol: false,
            lineStyle: { color: '#4ade80', width: 2 },
        },
        {
            name: 'Outbound',
            data: [],
            type: 'line',
            smooth: true,
            showSymbol: false,
            lineStyle: { color: '#60a5fa', width: 2 },
        }
    ]
  }
  networkChart.setOption(option)
}

function updateNetworkChart(metrics: any[]) {
    if (!networkChart) return
    const inData = metrics.map(m => (m.avg_net_in || 0).toFixed(2))
    const outData = metrics.map(m => (m.avg_net_out || 0).toFixed(2))
    const labels = metrics.map(m => {
        const d = new Date(m.timestamp * 1000)
        return d.getHours().toString().padStart(2, '0') + ':' + d.getMinutes().toString().padStart(2, '0') + ':' + d.getSeconds().toString().padStart(2, '0')
    })

    networkChart.setOption({
        xAxis: { data: labels },
        series: [
            { data: inData },
            { data: outData }
        ]
    })
}

function handleResize() {
  cpuChart?.resize()
  memoryChart?.resize()
  networkChart?.resize()
}

// Watch props.history
watch(() => props.history, (newMetrics) => {
  if (newMetrics && newMetrics.length > 0) {
    const chartData = [...newMetrics].sort((a,b) => a.timestamp - b.timestamp)
    updateCpuChart(chartData)
    updateMemoryChart(chartData)
    updateNetworkChart(chartData)
  } else {
    updateCpuChart([])
    updateMemoryChart([])
    updateNetworkChart([])
  }
}, { deep: true, immediate: true })

onMounted(() => {
  nextTick(() => {
     renderCpuChart()
     renderMemoryChart()
     renderNetworkChart()
     if (props.history && props.history.length > 0) {
         const chartData = [...props.history].sort((a,b) => a.timestamp - b.timestamp)
         updateCpuChart(chartData)
         updateMemoryChart(chartData)
         updateNetworkChart(chartData)
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
