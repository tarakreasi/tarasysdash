<template>
  <div class="flex flex-col h-screen overflow-hidden bg-background-light dark:bg-background-dark text-slate-900 dark:text-white font-display antialiased selection:bg-primary selection:text-black">
    <!-- Main Layout -->
    <div class="flex flex-1 overflow-hidden relative h-screen">
      <!-- Scanline Overlay -->
      <div class="absolute inset-0 scanline z-10 pointer-events-none opacity-20"></div>
      
      <!-- Main Content Area -->
      <main class="flex-1 flex flex-col min-w-0 overflow-hidden bg-background-dark">
        <div class="p-6 h-full flex flex-col">
          <!-- Section Header with Logo -->
          <div class="flex items-center justify-between mb-4 border-b border-border-color pb-2 shrink-0">
            <!-- Left: Logo + Section Title -->
            <div class="flex items-center gap-3 w-1/3">
              <div class="size-6 text-primary animate-pulse">
                <svg fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                  <path d="M42.4379 44C42.4379 44 36.0744 33.9038 41.1692 24C46.8624 12.9336 42.2078 4 42.2078 4L7.01134 4C7.01134 4 11.6577 12.932 5.96912 23.9969C0.876273 33.9029 7.27094 44 7.27094 44L42.4379 44Z" fill="currentColor"></path>
                </svg>
              </div>
              <h1 class="text-slate-400 text-sm font-bold tracking-tight uppercase">Overview Metrics</h1>
            </div>

            <!-- Center: App Title -->
            <div class="flex justify-center w-1/3">
              <h2 class="text-white text-lg font-bold tracking-wider uppercase drop-shadow-[0_0_5px_rgba(37,209,244,0.5)]">
                taraSysDash
              </h2>
            </div>
            
            <!-- Right: System Status -->
            <div class="flex items-center justify-end gap-3 w-1/3">
               <div class="hidden lg:flex items-center gap-2 px-2 py-0.5 bg-black/30 rounded border border-white/10">
                <span class="w-1.5 h-1.5 bg-green-500 rounded-full shadow-[0_0_5px_#22c55e]"></span>
                <span class="text-[10px] text-slate-300 font-mono">ONLINE</span>
              </div>
              <span class="text-primary font-mono text-xs">UPDATED: <span class="text-white">{{ lastUpdate || 'NOW' }}</span></span>
            </div>
          </div>
          
          <!-- Content Scroll Area -->
          <div class="flex-1 overflow-y-auto pr-2 scroll-smooth">
            <!-- Stats Grid -->
            <!-- Stats Grid -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <MetricCard 
              title="CPU Load" 
              icon="⚡" 
              :value="cpuLoad" 
              unit="%" 
              :trend="cpuTrend" 
              :percent="cpuLoad" 
              variant="primary" 
            />
            
            <MetricCard 
              title="Memory" 
              icon="💾" 
              :value="memoryGB" 
              unit="GB" 
              subtext="stable" 
              :percent="38" 
              variant="purple" 
            />
            
            <MetricCard 
              title="Net In" 
              icon="⬇️" 
              :value="netInMbps" 
              unit="MB/s" 
              :trend="12" 
              :percent="65" 
              variant="green" 
            />
            
            <MetricCard 
              title="Net Out" 
              icon="⬆️" 
              :value="netOutMbps" 
              unit="GB/s" 
              :trend="-5" 
              :percent="80" 
              variant="orange" 
            />
          </div>
          
          <!-- Charts Section -->
          <div class="grid grid-cols-1 xl:grid-cols-2 gap-6 mb-6">
            <div class="flex flex-col gap-4 rounded-xl bg-surface-dark/60 backdrop-blur-sm p-6 border border-border-color shadow-lg hover:shadow-[0_0_15px_rgba(37,209,244,0.15)] transition-all">
              <div class="flex justify-between items-center">
                <div>
                  <p class="text-slate-400 text-sm font-medium uppercase tracking-wider">CPU Load (Last 1hr)</p>
                  <p class="text-white text-2xl font-bold mt-1">{{ cpuLoad }}% <span class="text-sm font-normal text-slate-500">avg</span></p>
                </div>
                <div class="flex gap-2">
                  <span class="w-3 h-3 rounded-full bg-primary shadow-[0_0_8px_#25d1f4]"></span>
                  <span class="text-xs text-slate-400">Cluster A</span>
                </div>
              </div>
              <div id="cpu-chart" class="relative h-[200px] w-full"></div>
            </div>
            
            <div class="flex flex-col gap-4 rounded-xl bg-surface-dark/60 backdrop-blur-sm p-6 border border-border-color shadow-lg hover:shadow-[0_0_15px_rgba(168,85,247,0.15)] transition-all">
              <div class="flex justify-between items-center">
                <div>
                  <p class="text-slate-400 text-sm font-medium uppercase tracking-wider">Memory Usage</p>
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
          
          <!-- Server Detail Panel -->
          <div class="flex flex-col rounded-xl border border-border-color bg-surface-dark/80 backdrop-blur-md shadow-[0_0_20px_rgba(0,0,0,0.5)] overflow-hidden">
            <div class="flex items-center justify-between px-4 py-3 border-b border-border-color bg-surface-dark/50">
              <div class="flex items-center gap-2">
                <span class="text-primary text-[20px]">🖥️</span>
                <h3 class="text-sm font-bold uppercase tracking-widest text-white">
                  {{ selectedServer ? selectedServer.hostname : 'Server Details' }}
                </h3>
                <span v-if="selectedServer" class="text-xs text-slate-500 ml-2">{{ selectedServer.rack }} • {{ selectedServer.ip }}</span>
              </div>
              <div v-if="selectedServer" class="flex items-center gap-2">
                <span :class="getStatusBadgeClass(selectedServer.status)" class="px-2 py-1 rounded text-xs font-bold uppercase">
                  {{ selectedServer.status }}
                </span>
              </div>
            </div>
            
            <!-- Server Metrics Content -->
            <div v-if="selectedServer && selectedServerMetrics" class="p-6">
              <!-- Visual Gauges Grid -->
              <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
                <ServerGauge 
                  title="CPU Load" 
                  :value="parseFloat(selectedServerMetrics.cpu)" 
                  variant="cpu" 
                />
                
                <ServerGauge 
                  title="Memory" 
                  :value="(parseFloat(selectedServerMetrics.memoryUsed) / parseFloat(selectedServerMetrics.memoryTotal)) * 100" 
                  unit="GB"
                  variant="ram" 
                  :detail-formatter="() => `${selectedServerMetrics!.memoryUsed}GB\n${selectedServerMetrics!.memoryTotal}GB`"
                />

                <ServerGauge 
                  title="Temperature" 
                  :value="selectedServerMetrics.temp" 
                  variant="temp" 
                  unit="°C"
                />
              </div>

              <!-- Disk, Network, System Info Grid -->
              <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <!-- Disk Donut -->
                <ServerGauge 
                  title="Disk Usage" 
                  :value="(parseFloat(selectedServerMetrics.diskUsed) / parseFloat(selectedServerMetrics.diskTotal)) * 100" 
                  variant="disk" 
                  :detail-formatter="() => `${selectedServerMetrics!.diskUsed}GB\n${selectedServerMetrics!.diskTotal}GB`"
                />

                <!-- Network Stats -->
                <div class="bg-background-dark border border-border-color rounded-lg p-6 flex flex-col justify-center">
                  <div class="flex items-center justify-between mb-4">
                    <span class="text-sm text-slate-400 uppercase tracking-wider font-bold">Network I/O</span>
                    <span class="text-xl">📡</span>
                  </div>
                  <div class="space-y-6">
                    <div>
                      <div class="flex justify-between text-xs mb-1">
                        <span class="text-slate-500">Inbound</span>
                        <span class="text-green-400 font-mono">{{ selectedServerMetrics.netInDisplay }} MB/s</span>
                      </div>
                      <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                        <div class="bg-green-400 h-full" :style="`width: ${Math.min(selectedServerMetrics.netIn * 10, 100)}%`"></div>
                      </div>
                    </div>
                    <div>
                      <div class="flex justify-between text-xs mb-1">
                        <span class="text-slate-500">Outbound</span>
                        <span class="text-blue-400 font-mono">{{ selectedServerMetrics.netOutDisplay }} MB/s</span>
                      </div>
                      <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                        <div class="bg-blue-400 h-full" :style="`width: ${Math.min(selectedServerMetrics.netOut * 10, 100)}%`"></div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- System Info -->
                <div class="bg-background-dark border border-border-color rounded-lg p-6 flex flex-col justify-center">
                  <div class="flex items-center justify-between mb-4">
                    <span class="text-sm text-slate-400 uppercase tracking-wider font-bold">System Info</span>
                    <span class="text-xl">ℹ️</span>
                  </div>
                  <div class="space-y-4 text-sm">
                    <div class="flex justify-between border-b border-white/5 pb-2">
                      <span class="text-slate-500">OS:</span>
                      <span class="text-white font-mono">{{ selectedServer.os }}</span>
                    </div>
                    <div class="flex justify-between border-b border-white/5 pb-2">
                      <span class="text-slate-500">Uptime:</span>
                      <span class="text-white font-mono">{{ selectedServerMetrics.uptime }}</span>
                    </div>
                    <div class="flex justify-between">
                      <span class="text-slate-500">Processes:</span>
                      <span class="text-white font-mono">{{ selectedServerMetrics.processes }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Services Status -->
              <div class="bg-background-dark border border-border-color rounded-lg p-4 mt-4" v-if="selectedServerMetrics.services && selectedServerMetrics.services.length > 0">
                <div class="flex items-center justify-between mb-3">
                  <span class="text-sm text-slate-400 uppercase tracking-wider font-bold">Services</span>
                  <span class="text-xl">⚙️</span>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-sm">
                  <div v-for="svc in selectedServerMetrics.services" :key="svc.name" class="flex justify-between items-center bg-slate-800/50 p-2 rounded">
                    <span class="text-slate-300">{{ svc.name }}</span>
                    <span :class="svc.running ? 'text-green-400' : 'text-red-400'" class="font-mono text-xs uppercase border border-white/10 px-1 rounded">
                      {{ svc.running ? 'RUNNING' : 'STOPPED' }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Empty State -->
            <div v-else class="flex flex-col items-center justify-center py-16 text-center">
              <div class="text-6xl mb-4 opacity-50">👈</div>
              <h3 class="text-lg font-bold text-white mb-2">Select a Server</h3>
              <p class="text-sm text-slate-400">Click on any server in the sidebar to view detailed metrics</p>
            </div>
          </div>
          </div>
        </div>
      </main>
      
      <!-- Right Sidebar (Server Rack Status) -->
      <aside class="w-full lg:w-80 border-l border-border-color bg-surface-dark overflow-y-auto hidden lg:flex flex-col">
        <!-- Sidebar Header with Actions -->
        <div class="px-5 py-4 border-b border-border-color bg-surface-dark sticky top-0 z-10 flex flex-col gap-4">
           <!-- Action Buttons (Moved from Header) -->
           <div class="flex justify-end gap-2">
            <button class="flex items-center justify-center rounded-lg h-8 w-8 bg-surface-dark border border-border-color hover:border-primary text-slate-300 hover:text-primary transition-all">
              <span class="text-[18px]">⚙️</span>
            </button>
            <button class="flex items-center justify-center rounded-lg h-8 w-8 bg-surface-dark border border-border-color hover:border-primary text-slate-300 hover:text-primary transition-all relative">
              <span class="text-[18px]">🔔</span>
              <span class="absolute top-1.5 right-1.5 w-1.5 h-1.5 bg-red-500 rounded-full"></span>
            </button>
            <button class="flex items-center justify-center rounded-lg h-8 w-8 bg-primary text-black font-bold">
              <span class="text-[18px]">👤</span>
            </button>
          </div>

          <h3 class="text-white text-lg font-bold leading-tight tracking-tight flex items-center gap-2">
            <span class="text-primary text-2xl">🖥️</span>
            Rack Status
          </h3>
        </div>
        <div class="p-4 grid gap-3">
          <!-- Server Items -->
          <div 
            v-for="server in sidebarServers" 
            :key="server.id"
            :class="[
              getServerCardClass(server.status),
              selectedServer?.id === server.id ? 'ring-2 ring-primary bg-primary/10' : ''
            ]"
            class="flex gap-3 rounded-lg p-3 items-center transition-all cursor-pointer group"
            @click="selectServer(server)"
          >
            <span :class="getStatusIconClass(server.status)" class="text-[20px]">{{ getStatusIcon(server.status) }}</span>
            <div class="flex flex-col flex-1 min-w-0">
              <div class="flex items-center justify-between">
                <h2 class="text-white text-sm font-bold leading-tight font-mono truncate">{{ server.hostname }}</h2>
                <button 
                  @click.stop="handleEditServer(server)"
                  class="text-slate-500 hover:text-primary opacity-0 group-hover:opacity-100 transition-opacity p-1 ml-2"
                  title="Edit Server"
                >
                  ✏️
                </button>
              </div>
              <span class="text-[10px] text-slate-500">{{ server.rack }} • {{ server.temp }}°C</span>
            </div>
          </div>
          
          <!-- Empty State -->
          <div v-if="sidebarServers.length === 0" class="text-center py-8 text-slate-500 text-sm">
            <div class="text-4xl mb-2 opacity-50">📡</div>
            <p>No agents online</p>
          </div>
        </div>
        
        <!-- Total Capacity Footer -->
        <div class="mt-auto p-4 border-t border-border-color bg-background-dark/50">
          <div class="rounded bg-slate-800 p-2 text-center">
            <p class="text-[10px] uppercase text-slate-400 tracking-widest mb-1">Total Capacity</p>
            <div class="w-full bg-slate-900 h-2 rounded-full overflow-hidden">
              <div class="bg-primary h-full" :style="`width: ${totalCapacity}%`"></div>
            </div>
            <p class="text-xs font-mono text-primary mt-1 text-right">{{ totalCapacity }}%</p>
          </div>
        </div>
      </aside>
    </div>

    <!-- Modals -->
    <EditServerModal 
      :is-open="isEditModalOpen" 
      :server="editingServer" 
      @close="isEditModalOpen = false" 
      @save="handleSaveServer"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts/core'
import { LineChart, BarChart, GaugeChart, PieChart } from 'echarts/charts'
import { GridComponent, TooltipComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import EditServerModal from '../components/EditServerModal.vue'
import MetricCard from '../components/MetricCard.vue'
import ServerGauge from '../components/ServerGauge.vue'
import { useDashboard } from '../composables/useDashboard'
import { 
  getStatusBadgeClass, 
  getStatusIcon, 
  getStatusIconClass, 
  getServerCardClass 
} from '../utils/formatters'

echarts.use([LineChart, BarChart, GaugeChart, PieChart, GridComponent, TooltipComponent, CanvasRenderer])

// --- Composable ---
const {
  // State
  cpuLoad,
  cpuTrend,
  memoryGB,
  netInMbps,
  netOutMbps,
  lastUpdate,
  selectedServer,
  isEditModalOpen,
  editingServer,
  selectedServerMetrics,
  sidebarServers,
  totalCapacity,
  
  // Actions
  fetchServers,
  fetchMetrics,
  fetchAgentMetrics,
  selectServer,
  handleEditServer,
  handleSaveServer
} = useDashboard()

// --- Charts ---
let cpuChart: echarts.ECharts | null = null
let memoryChart: echarts.ECharts | null = null
let updateInterval: number | null = null

// --- Chart Rendering ---
function renderCpuChart() {
  const dom = document.getElementById('cpu-chart')
  if (!dom) return
  if (!cpuChart) cpuChart = echarts.init(dom)
  
  // Generate CPU history data (mock)
  const history = Array.from({length: 30}, () => Math.floor(Math.random() * 30 + 40))
  
  const option = {
    grid: { left: 0, right: 0, top: 10, bottom: 0 },
    xAxis: { type: 'category', show: false },
    yAxis: { type: 'value', show: false },
    tooltip: { trigger: 'axis' },
    series: [{
      data: history,
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

function renderMemoryChart() {
   const dom = document.getElementById('memory-chart')
   if (!dom) return
   if (!memoryChart) memoryChart = echarts.init(dom)

   // Generate RAM usage data (mock)
   const data = Array.from({length: 30}, () => Math.floor(Math.random() * 2 + 6))
   
   const option = {
    grid: { left: 0, right: 0, top: 10, bottom: 0 },
    xAxis: { type: 'category', show: false },
    yAxis: { type: 'value', show: false, min: 0 },
    tooltip: { trigger: 'axis' },
    series: [{
      data: data,
      type: 'bar',
      itemStyle: { color: '#a855f7', borderRadius: [2, 2, 0, 0] }
    }]
  }
  memoryChart.setOption(option)
}


function handleResize() {
  cpuChart?.resize()
  memoryChart?.resize()
}

// --- Lifecycle ---
onMounted(async () => {
  await fetchServers()
  await fetchMetrics() // Initial fetch
  
  // Wait for DOM
  nextTick(() => {
     renderCpuChart() // Initial CPU chart
     renderMemoryChart() // Initial Memory chart
  })

  updateInterval = window.setInterval(async () => {
    await fetchServers()
    await fetchMetrics()
    if (selectedServer.value) {
      await fetchAgentMetrics(selectedServer.value.id)
    }
    lastUpdate.value = new Date().toLocaleTimeString()
    renderCpuChart() // Refresh CPU chart
    renderMemoryChart() // Refresh Memory chart
  }, 2000)

  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  if (updateInterval) clearInterval(updateInterval)
  window.removeEventListener('resize', handleResize)
  cpuChart?.dispose()
  memoryChart?.dispose()
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

/* Scanline effect for cyberpunk aesthetic */
.scanline {
  background: linear-gradient(to bottom,
    rgba(255, 255, 255, 0),
    rgba(255, 255, 255, 0) 50%,
    rgba(0, 0, 0, 0.1) 50%,
    rgba(0, 0, 0, 0.1));
  background-size: 100% 4px;
  pointer-events: none;
}

/* Terminal text font */
.terminal-text {
  font-family: 'Courier New', Courier, monospace;
}

/* Scrollbar Polish */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: #101f22; 
}
::-webkit-scrollbar-thumb {
  background: #283639; 
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
  background: #25d1f4; 
}
</style>
