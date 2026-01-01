<template>
  <div class="flex h-screen overflow-hidden">
    <!-- Left Panel: Overview Metrics -->
    <div class="flex-1 p-6 overflow-y-auto">
      <div class="flex items-center justify-between mb-6">
        <h1 class="text-2xl font-bold">Overview Metrics</h1>
        <p class="text-xs text-slate-400">LAST UPDATED: {{ lastUpdate }}</p>
      </div>

      <!-- Row 1: Core Metrics (4 cards) -->
      <div class="grid grid-cols-4 gap-4 mb-4">
        <!-- CPU Load -->
        <div class="bg-surface-dark border border-border-color rounded-lg p-4">
          <div class="flex items-start justify-between mb-2">
            <p class="text-xs text-slate-400 uppercase tracking-wide">CPU LOAD</p>
            <span class="text-xl">⚡</span>
          </div>
          <p class="text-3xl font-bold mb-1">{{ cpuLoad }}%</p>
          <div class="flex items-center text-xs" :class="cpuTrend >= 0 ? 'text-green-500' : 'text-red-500'">
            <span>{{ cpuTrend >= 0 ? '+' : '' }}{{ cpuTrend }}%</span>
          </div>
        </div>

        <!-- Memory -->
        <div class="bg-surface-dark border border-border-color rounded-lg p-4">
          <div class="flex items-start justify-between mb-2">
            <p class="text-xs text-slate-400 uppercase tracking-wide">MEMORY</p>
            <span class="text-xl">💾</span>
          </div>
          <p class="text-3xl font-bold mb-1">{{ memoryGB }} <span class="text-sm text-slate-400">GB</span></p>
          <p class="text-xs text-slate-400">stable</p>
        </div>

        <!-- Net In -->
        <div class="bg-surface-dark border border-border-color rounded-lg p-4">
          <div class="flex items-start justify-between mb-2">
            <p class="text-xs text-slate-400 uppercase tracking-wide">NET IN</p>
            <span class="text-xl">⬇️</span>
          </div>
          <p class="text-3xl font-bold mb-1">{{ netInMbps }} <span class="text-sm text-slate-400">MB/s</span></p>
          <div class="flex items-center text-xs text-green-500">
            <span>+{{ netInSpeed }}%</span>
          </div>
        </div>

        <!-- Net Out -->
        <div class="bg-surface-dark border border-border-color rounded-lg p-4">
          <div class="flex items-start justify-between mb-2">
            <p class="text-xs text-slate-400 uppercase tracking-wide">NET OUT</p>
            <span class="text-xl">⬆️</span>
          </div>
          <p class="text-3xl font-bold mb-1">{{ netOutMbps }} <span class="text-sm text-slate-400">MB/s</span></p>
          <div class="flex items-center text-xs text-red-500">
            <span>+{{ netOutSpeed }}%</span>
          </div>
        </div>
      </div>

      <!-- Row 2: Charts -->
      <div class="grid grid-cols-2 gap-4 mb-4">
        <!-- Latency Chart -->
        <div class="bg-surface-dark border border-border-color rounded-lg p-4">
          <div class="flex items-center justify-between mb-3">
            <div>
              <p class="text-xs text-slate-400 uppercase tracking-wide">LATENCY (LAST 10H)</p>
              <p class="text-2xl font-bold mt-1">{{ avgLatency }}<span class="text-sm text-slate-400">ms avg</span></p>
            </div>
          </div>
          <div id="latency-chart" class="h-32"></div>
        </div>

        <!-- Throughput Chart -->
        <div class="bg-surface-dark border border-border-color rounded-lg p-4">
          <div class="flex items-center justify-between mb-3">
            <div>
              <p class="text-xs text-slate-400 uppercase tracking-wide">THROUGHPUT (RPS)</p>
              <p class="text-2xl font-bold mt-1">{{ throughput }}<span class="text-sm text-slate-400"> ops</span></p>
            </div>
          </div>
          <div id="throughput-chart" class="h-32"></div>
        </div>
      </div>

      <!-- Row 3: Live System Logs -->
      <div class="bg-surface-dark border border-border-color rounded-lg p-4">
        <div class="flex items-center justify-between mb-3">
          <p class="text-xs text-slate-400 uppercase tracking-wide">🟢 LIVE SYSTEM LOGS</p>
          <div class="flex gap-2 text-xs">
            <button class="text-primary hover:underline">ALL</button>
            <button class="text-slate-400 hover:text-primary">ERROR</button>
            <button class="text-slate-400 hover:text-primary">WARN</button>
          </div>
        </div>
        <div class="font-mono text-xs space-y-1 h-40 overflow-y-auto">
          <p v-for="(log, i) in logs" :key="i" :class="getLogClass(log.level)">
            [{{ log.time }}] <span :class="getLogLevelClass(log.level)">[{{ log.level }}]</span> {{ log.message }}
          </p>
        </div>
      </div>
    </div>

    <!-- Right Sidebar: Server List -->
    <div class="w-80 bg-surface-dark border-l border-border-color p-4 overflow-y-auto">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-sm font-bold uppercase tracking-wide">Rack Status</h2>
        <span class="text-xs text-slate-400">{{ servers.length }} servers</span>
      </div>
      
      <div class="space-y-2">
        <div v-for="server in servers" :key="server.id" 
             class="flex items-center gap-3 p-2 rounded hover:bg-background-dark/50 cursor-pointer transition">
          <div class="size-2 rounded-full" :class="server.status === 'online' ? 'bg-green-500' : server.status === 'warning' ? 'bg-yellow-500' : 'bg-red-500'"></div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium truncate">{{ server.name }}</p>
            <p class="text-xs text-slate-400">{{ server.rack }} • {{ server.temp }}°C</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import * as echarts from 'echarts/core'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

echarts.use([LineChart, GridComponent, TooltipComponent, CanvasRenderer])

const API_BASE = 'http://localhost:8080/api/v1'

const cpuLoad = ref(45)
const cpuTrend = ref(2)
const memoryGB = ref(12.4)
const netInMbps = ref(450)
const netInSpeed = ref(40)
const netOutMbps = ref(1.2)
const netOutSpeed = ref(10)
const avgLatency = ref(14)
const throughput = ref(4500)
const lastUpdate = ref('NOW')

const logs = ref([
  { time: '14:05:31', level: 'INFO', message: 'Cron job maintenance_daily executed successfully.' },
  { time: '14:04:05', level: 'INFO', message: 'Daily backup sequence initiated on db-shard-04.' },
  { time: '14:01:23', level: 'WARN', message: 'High latency detected on srv-us-e-04 (240ms).' },
  { time: '13:58:42', level: 'ERROR', message: 'Failed polling pod payment-service-v3 (replicas: 4 -> 5).' },
  { time: '13:54:10', level: 'INFO', message: 'User admin #1 logged in from 192.168.1.45.' },
  { time: '13:50:38', level: 'INFO', message: 'Alert connection timeout external API gateway (Retry 1/3).' },
  { time: '13:51:11', level: 'INFO', message: 'SSH session check listed for all critical services.' },
])

const servers = ref([
  { id: 1, name: 'srv-us-e-01', rack: 'Rack A1', temp: 45, status: 'online' },
  { id: 2, name: 'srv-us-e-02', rack: 'Rack A1', temp: 42, status: 'online' },
  { id: 3, name: 'srv-us-e-03', rack: 'Rack A2', temp: 67, status: 'warning' },
  { id: 4, name: 'srv-us-e-04', rack: 'Rack A2', temp: 38, status: 'online' },
  { id: 5, name: 'srv-us-e-05', rack: 'Rack A3', temp: 44, status: 'online' },
  { id: 6, name: 'srv-du-c-01', rack: 'Rack B1', temp: 48, status: 'online' },
  { id: 7, name: 'srv-du-c-02', rack: 'Rack B1', temp: 91, status: 'error' },
  { id: 8, name: 'srv-du-c-03', rack: 'Rack B2', temp: 43, status: 'online' },
])

let latencyChart: echarts.ECharts | null = null
let throughputChart: echarts.ECharts | null = null
let updateInterval: number | null = null

function getLogClass(level: string) {
  return 'text-slate-300'
}

function getLogLevelClass(level: string) {
  if (level === 'ERROR') return 'text-red-500'
  if (level === 'WARN') return 'text-yellow-500'
  return 'text-primary'
}

async function fetchRealData() {
  try {
    const agents = await axios.get(`${API_BASE}/agents`)
    if (agents.data && agents.data.length > 0) {
      const agentId = agents.data[0].id
      
      // Fetch metrics
      const metrics = await axios.get(`${API_BASE}/metrics/${agentId}`)
      if (metrics.data && metrics.data.length > 0) {
        const latest = metrics.data[metrics.data.length - 1]
        cpuLoad.value = parseFloat(latest.cpu_usage_percent.toFixed(1))
        memoryGB.value = parseFloat((latest.memory_used_bytes / 1073741824).toFixed(1))
      }

      // Fetch network stats
      const networkStats = await axios.get(`${API_BASE}/stats/${agentId}/network`)
      if (networkStats.data) {
        netInMbps.value = parseFloat(networkStats.data.avg_mbps_in.toFixed(0))
        netOutMbps.value = parseFloat(networkStats.data.avg_mbps_out.toFixed(2))
      }

      // Fetch latency stats
      const latencyStats = await axios.get(`${API_BASE}/stats/${agentId}/latency`)
      if (latencyStats.data) {
        avgLatency.value = parseFloat(latencyStats.data.avg_latency_ms.toFixed(0))
        renderLatencyChart(latencyStats.data.history)
      }
    }
  } catch (err) {
    console.error('Failed to fetch real data:', err)
  }
}

function renderLatencyChart(history: number[]) {
  const chartDom = document.getElementById('latency-chart')
  if (!chartDom) return

  if (!latencyChart) {
    latencyChart = echarts.init(chartDom)
  }

  const option = {
    grid: { left: 40, right: 10, top: 10, bottom: 20 },
    xAxis: { type: 'category', show: false },
    yAxis: { type: 'value', show: false },
    series: [{
      data: history.slice(-60),
      type: 'line',
      smooth: true,
      lineStyle: { color: '#25d1f4', width: 2 },
      areaStyle: { color: 'rgba(37, 209, 244, 0.1)' }
    }]
  }

  latencyChart.setOption(option)
}

function renderThroughputChart() {
  const chartDom = document.getElementById('throughput-chart')
  if (!chartDom) return

  if (!throughputChart) {
    throughputChart = echarts.init(chartDom)
  }

  const option = {
    grid: { left: 40, right: 10, top: 10, bottom: 20 },
    xAxis: { type: 'category', show: false },
    yAxis: { type: 'value', show: false },
    series: [
      {
        name: 'HTTP',
        data: Array.from({ length: 60 }, () => Math.random() * 5000 + 3000),
        type: 'line',
        smooth: true,
        lineStyle: { color: '#25d1f4', width: 2 }
      },
      {
        name: 'gRPC',
        data: Array.from({ length: 60 }, () => Math.random() * 2000 + 1000),
        type: 'line',
        smooth: true,
        lineStyle: { color: '#4caf50', width: 2 }
      }
    ]
  }

  throughputChart.setOption(option)
}

onMounted(async () => {
  await fetchRealData()
  renderThroughputChart()
  
  updateInterval = window.setInterval(() => {
    fetchRealData()
    lastUpdate.value = new Date().toLocaleTimeString()
  }, 5000)
})

onUnmounted(() => {
  if (updateInterval) clearInterval(updateInterval)
  latencyChart?.dispose()
  throughputChart?.dispose()
})
</script>
