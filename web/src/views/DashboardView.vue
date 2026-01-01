<template>
  <div class="flex flex-col h-screen overflow-hidden bg-background">
    <!-- Top Bar / Header -->
    <div class="flex items-center justify-between px-6 py-4 border-b border-border-color bg-surface-dark">
      <div class="flex items-center gap-4">
        <h1 class="text-xl font-bold tracking-tight">TaraSysDash <span class="text-primary text-xs ml-1">v0.3.0</span></h1>
        <div class="h-4 w-px bg-border-color"></div>
        <div class="flex items-center gap-2 text-xs text-slate-400">
          <span class="size-2 rounded-full bg-green-500 animate-pulse"></span>
          <span>System Online</span>
        </div>
      </div>
      <div class="flex items-center gap-4 text-xs font-mono text-slate-400">
         <span>AGENTS: <span class="text-white">{{ servers.length }}</span></span>
         <span>|</span>
         <span>LAST UPDATE: {{ lastUpdate }}</span>
      </div>
    </div>

    <!-- Main Scrollable Content -->
    <div class="flex-1 overflow-y-auto p-6 space-y-6">
      
      <!-- Section 1: Aggregate Metrics (Top Cards) -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <!-- CPU Load -->
        <div class="bg-surface-dark border border-border-color rounded-lg p-4 relative overflow-hidden group hover:border-primary/50 transition-all">
          <div class="flex justify-between items-start">
            <p class="text-xs text-slate-400 uppercase tracking-wide mb-1">AVG CPU LOAD</p>
            <span class="text-2xl opacity-50 group-hover:opacity-100 transition-opacity">⚡</span>
          </div>
          <div class="flex items-end gap-2">
            <span class="text-3xl font-bold">{{ cpuLoad }}%</span>
            <span class="text-xs mb-1" :class="cpuTrend >= 0 ? 'text-green-500' : 'text-red-500'">
              {{ cpuTrend >= 0 ? '↑' : '↓' }} {{ Math.abs(cpuTrend) }}%
            </span>
          </div>
          <div class="w-full bg-slate-800 h-1 mt-2 rounded-full overflow-hidden">
            <div class="bg-primary h-full transition-all" :style="`width: ${cpuLoad}%; box-shadow: 0 0 8px #25d1f4`"></div>
          </div>
        </div>

        <!-- Memory -->
        <div class="bg-surface-dark border border-border-color rounded-lg p-4 relative overflow-hidden group hover:border-primary/50 transition-all">
          <div class="flex justify-between items-start">
            <p class="text-xs text-slate-400 uppercase tracking-wider mb-1">MEMORY USAGE</p>
            <span class="text-2xl opacity-50 group-hover:opacity-100 transition-opacity">💾</span>
          </div>
          <div class="flex items-end gap-2">
            <span class="text-3xl font-bold leading-none">{{ memoryGB }}<span class="text-lg text-slate-500"> GB</span></span>
            <span class="text-sm text-slate-400 mb-1">avg</span>
          </div>
          <div class="w-full bg-slate-800 h-1 mt-2 rounded-full overflow-hidden">
            <div class="bg-purple-500 h-full w-[38%]" style="box-shadow: 0 0 8px #a855f7"></div>
          </div>
        </div>

        <!-- Net In -->
        <div class="bg-surface-dark border border-border-color rounded-lg p-4 relative overflow-hidden group">
           <div class="absolute top-0 right-0 p-3 opacity-10 group-hover:opacity-20 transition">
            <span class="text-6xl">⬇️</span>
          </div>
          <p class="text-xs text-slate-400 uppercase tracking-wide mb-1">NET INBOUND</p>
          <div class="flex items-end gap-2">
            <span class="text-3xl font-bold text-green-400">{{ netInMbps }}</span>
            <span class="text-sm text-slate-500 mb-1">Mbps</span>
          </div>
        </div>

        <!-- Net Out -->
        <div class="bg-surface-dark border border-border-color rounded-lg p-4 relative overflow-hidden group">
           <div class="absolute top-0 right-0 p-3 opacity-10 group-hover:opacity-20 transition">
            <span class="text-6xl">⬆️</span>
          </div>
          <p class="text-xs text-slate-400 uppercase tracking-wide mb-1">NET OUTBOUND</p>
           <div class="flex items-end gap-2">
            <span class="text-3xl font-bold text-blue-400">{{ netOutMbps }}</span>
            <span class="text-sm text-slate-500 mb-1">Mbps</span>
          </div>
        </div>
      </div>

      <!-- Section 2: Charts (Latency & Throughput) -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 h-48 md:h-48">
         <div class="bg-surface-dark border border-border-color rounded-lg p-4 flex flex-col">
            <div class="flex justify-between items-center mb-2">
              <h3 class="text-xs font-bold uppercase text-slate-400">Latency History (Global Avg)</h3>
              <span class="text-xs font-mono text-primary">{{ avgLatency }}ms</span>
            </div>
            <div id="latency-chart" class="flex-1 w-full min-h-0"></div>
         </div>
         <div class="bg-surface-dark border border-border-color rounded-lg p-4 flex flex-col">
             <div class="flex justify-between items-center mb-2">
              <h3 class="text-xs font-bold uppercase text-slate-400">Total Throughput</h3>
              <span class="text-xs font-mono text-green-400">{{ throughput }} ops/s</span>
            </div>
            <div id="throughput-chart" class="flex-1 w-full min-h-0"></div>
         </div>
      </div>

      <!-- Section 3: Server Grid (Grouped by Rack) -->
      <div class="space-y-6">
        
        <!-- Search Bar -->
        <div class="flex items-center gap-4 bg-surface-dark border border-border-color rounded-lg p-4">
          <svg class="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input 
            v-model="searchQuery"
            type="text" 
            placeholder="Search agents by name, IP, OS, rack, or status..."
            class="flex-1 bg-transparent text-white placeholder-slate-500 outline-none text-sm"
          />
          <span v-if="searchQuery" class="text-xs text-slate-500">
            {{ filteredServers.length }} / {{ servers.length }} agents
          </span>
        </div>

        <!-- Rack Groups -->
        <div v-for="rack in racks" :key="rack" class="animate-fade-in-up">
          <!-- Rack Header -->
          <div class="flex items-center gap-4 mb-4 cursor-pointer group" @click="toggleRack(rack)">
             <div class="h-px bg-border-color flex-1"></div>
             <h2 class="text-base font-bold uppercase tracking-widest text-slate-400 whitespace-nowrap group-hover:text-primary transition-colors">
                {{ rack || 'UNASSIGNED' }}
                <span class="text-xs ml-2 text-slate-500">({{ rackCount(rack) }} agents)</span>
                <span class="ml-2 text-sm">{{ collapsedRacks.has(rack) ? '▼' : '▲' }}</span>
             </h2>
             <div class="h-px bg-border-color flex-1"></div>
          </div>

          <!-- Server Cards Grid -->
          <div v-if="!collapsedRacks.has(rack)" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-3">
            <ServerCard 
              v-for="server in serversByRack(rack)" 
              :key="server.id"
              :server="server"
            />
          </div>

          <!-- Empty State for Filtered Results -->
          <div v-if="!collapsedRacks.has(rack) && rackCount(rack) === 0" class="text-center py-8 text-slate-500 text-sm">
            No agents match your search criteria
          </div>
        </div>

        <!-- Empty State for No Agents -->
        <div v-if="servers.length === 0" class="text-center py-12">
          <div class="text-6xl mb-4 opacity-50">📡</div>
          <p class="text-slate-400 text-sm">No agents registered yet</p>
        </div>
      </div>

       <!-- Section 4: Logs (Collapsible/Bottom) -->
       <div class="bg-surface-dark border border-border-color rounded-lg p-4 mt-8">
          <h3 class="text-xs font-bold uppercase text-slate-400 mb-2">Recent System Events</h3>
          <div class="font-mono text-[10px] text-slate-400 space-y-1 max-h-32 overflow-y-auto">
             <p v-for="(log, i) in logs" :key="i" class="hover:text-white transition-colors cursor-default">
               <span class="text-slate-600 mr-2">{{ log.time }}</span>
               <span :class="getLogLevelClass(log.level)" class="font-bold mr-2">[{{ log.level }}]</span>
               {{ log.message }}
             </p>
          </div>
       </div>

    </div>

  </div>
</template>

<script setup lang="ts">
// Type definitions
interface Server {
  id: string
  name: string
  hostname: string
  rack: string
  temp: number
  status: string
  ip: string
  os: string
}

import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import ServerCard from '../components/ServerCard.vue'
import axios from 'axios'
import * as echarts from 'echarts/core'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

echarts.use([LineChart, GridComponent, TooltipComponent, CanvasRenderer])

const API_BASE = 'http://localhost:8080/api/v1'

// --- State ---
const cpuLoad = ref(0)
const cpuTrend = ref(0)
const memoryGB = ref(0)
const netInMbps = ref(0)
const netOutMbps = ref(0)
const avgLatency = ref(0)
const throughput = ref(0)
const lastUpdate = ref('--:--:--')

const servers = ref<Server[]>([])
const searchQuery = ref('')
const collapsedRacks = ref<Set<string>>(new Set())

const logs = ref<any[]>([
  { time: '14:05:31', level: 'INFO', message: 'System initialized. Dashboard ready.' },
])

// --- Charts ---
let latencyChart: echarts.ECharts | null = null
let throughputChart: echarts.ECharts | null = null
let updateInterval: number | null = null

// --- Computed ---
// Numeric sorting helper
function extractNumber(id: string): number {
  const match = id.match(/\d+$/)
  return match ? parseInt(match[0], 10) : 0
}

const racks = computed(() => {
  const uniqueRacks = [...new Set(servers.value.map(s => s.rack))]
  return uniqueRacks.sort()
})

// Filtered servers based on search
const filteredServers = computed(() => {
  if (!searchQuery.value.trim()) return servers.value
  
  const query = searchQuery.value.toLowerCase()
  return servers.value.filter(s => 
    s.hostname.toLowerCase().includes(query) ||
    s.ip.toLowerCase().includes(query) ||
    s.os.toLowerCase().includes(query) ||
    s.rack.toLowerCase().includes(query) ||
    s.status.toLowerCase().includes(query)
  )
})

// Servers grouped by rack with numeric sorting
function serversByRack(rack: string) {
  return filteredServers.value
    .filter(s => s.rack === rack)
    .sort((a, b) => extractNumber(a.hostname) - extractNumber(b.hostname))
}

// Count agents per rack
function rackCount(rack: string): number {
  return serversByRack(rack).length
}

// Toggle rack collapse
function toggleRack(rack: string) {
  if (collapsedRacks.value.has(rack)) {
    collapsedRacks.value.delete(rack)
  } else {
    collapsedRacks.value.add(rack)
  }
}

function getLogLevelClass(level: string) {
  if (level === 'ERROR') return 'text-red-500'
  if (level === 'WARN') return 'text-yellow-500'
  return 'text-blue-400'
}

// --- Actions ---
async function fetchServers() {
  try {
    const response = await axios.get(`${API_BASE}/agents`)
    if (response.data) {
      servers.value = response.data.map((agent: any) => ({
        id: agent.id,
        name: agent.hostname,
        hostname: agent.hostname,
        rack: agent.rack_location || 'Unassigned',
        temp: agent.temperature || 0,
        status: agent.status || 'offline',
        ip: agent.ip_address,
        os: agent.os
      }))
    }
  } catch (err) {
    console.error('Failed to fetch servers:', err)
  }
}

async function fetchMetrics() {
  // Aggregate metrics from all active servers
  // In a real app, the backend should provide an aggregate endpoint.
  // For MVP, we'll scan the top 5 active servers or just one for demo
  try {
      if (servers.value.length === 0) return

      // Just grab metrics from the first active server for the "Global" view simulation
      // Or ideally, fetch /stats/global if it existed.
      // We will sum up throughput and avg latency from top agent for now as a proxy
      const active = servers.value.find(s => s.status === 'online')
      if (active) {
          const m = await axios.get(`${API_BASE}/metrics/${active.id}`)
          if (m.data && m.data.length > 0) {
              const latest = m.data[m.data.length-1]
              cpuLoad.value = parseFloat(latest.cpu_usage_percent.toFixed(1))
              memoryGB.value = parseFloat((latest.memory_used_bytes / 1073741824).toFixed(1))
              throughput.value = Math.floor(Math.random() * 500 + 4000) // Mock fluctuation
          }
           
          const lat = await axios.get(`${API_BASE}/stats/${active.id}/latency`)
          if (lat.data) {
             avgLatency.value = parseFloat(lat.data.avg_latency_ms.toFixed(0))
             renderLatencyChart(lat.data.history)
          }
      }
  } catch (e) { console.error(e) }
}


// --- Chart Rendering ---
function renderLatencyChart(history: number[]) {
  const dom = document.getElementById('latency-chart')
  if (!dom) return
  if (!latencyChart) latencyChart = echarts.init(dom)
  
  const option = {
    grid: { left: 0, right: 0, top: 10, bottom: 0 },
    xAxis: { type: 'category', show: false },
    yAxis: { type: 'value', show: false },
    tooltip: { trigger: 'axis' },
    series: [{
      data: history?.slice(-30) || [],
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
  latencyChart.setOption(option)
}

function renderThroughputChart() {
   const dom = document.getElementById('throughput-chart')
   if (!dom) return
   if (!throughputChart) throughputChart = echarts.init(dom)

   const data = Array.from({length: 30}, () => Math.floor(Math.random() * 1000 + 3000))
   
   const option = {
    grid: { left: 0, right: 0, top: 10, bottom: 0 },
    xAxis: { type: 'category', show: false },
    yAxis: { type: 'value', show: false, min: 2000 },
    tooltip: { trigger: 'axis' },
    series: [{
      data: data,
      type: 'bar',
      itemStyle: { color: '#4caf50', borderRadius: [2, 2, 0, 0] }
    }]
  }
  throughputChart.setOption(option)
}

function handleResize() {
  latencyChart?.resize()
  throughputChart?.resize()
}

// --- Lifecycle ---
onMounted(async () => {
  await fetchServers()
  await fetchMetrics() // Initial fetch
  
  // Wait for DOM
  nextTick(() => {
     renderThroughputChart() // Initial dummy render
  })

  updateInterval = window.setInterval(async () => {
    await fetchServers()
    await fetchMetrics()
    lastUpdate.value = new Date().toLocaleTimeString()
    renderThroughputChart() // Refresh dummy chart
  }, 2000)

  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  if (updateInterval) clearInterval(updateInterval)
  window.removeEventListener('resize', handleResize)
  latencyChart?.dispose()
  throughputChart?.dispose()
})
</script>

<style>
.animate-fade-in-up {
  animation: fadeInUp 0.5s ease-out;
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
/* Scrollbar Polish */
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-track {
  background: #0f172a; 
}
::-webkit-scrollbar-thumb {
  background: #334155; 
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #475569; 
}
</style>
