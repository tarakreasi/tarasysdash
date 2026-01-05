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
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <!-- CPU Card -->
            <div class="flex flex-col gap-2 rounded-xl bg-surface-dark p-5 border border-border-color shadow-lg hover:border-primary/50 transition-colors group">
              <div class="flex justify-between items-start">
                <p class="text-slate-400 text-sm font-medium uppercase tracking-wider">CPU Load</p>
                <span class="text-2xl opacity-50 group-hover:opacity-100 transition-opacity">⚡</span>
              </div>
              <div class="flex items-end gap-3 mt-2">
                <p class="text-white text-3xl font-bold leading-none tracking-tight">{{ cpuLoad }}%</p>
                <p class="text-green-500 text-sm font-medium flex items-center mb-1" v-if="cpuTrend >= 0">
                  <span class="text-[16px]">↑</span> {{ cpuTrend }}%
                </p>
              </div>
              <div class="w-full bg-slate-800 h-1 mt-2 rounded-full overflow-hidden">
                <div class="bg-primary h-full shadow-[0_0_8px_#25d1f4]" :style="`width: ${cpuLoad}%`"></div>
              </div>
            </div>
            
            <!-- Memory Card -->
            <div class="flex flex-col gap-2 rounded-xl bg-surface-dark p-5 border border-border-color shadow-lg hover:border-primary/50 transition-colors group">
              <div class="flex justify-between items-start">
                <p class="text-slate-400 text-sm font-medium uppercase tracking-wider">Memory</p>
                <span class="text-2xl opacity-50 group-hover:opacity-100 transition-opacity">💾</span>
              </div>
              <div class="flex items-end gap-3 mt-2">
                <p class="text-white text-3xl font-bold leading-none tracking-tight">{{ memoryGB }} <span class="text-lg text-slate-500">GB</span></p>
                <p class="text-slate-400 text-sm font-medium mb-1">stable</p>
              </div>
              <div class="w-full bg-slate-800 h-1 mt-2 rounded-full overflow-hidden">
                <div class="bg-purple-500 h-full w-[38%] shadow-[0_0_8px_#a855f7]"></div>
              </div>
            </div>
            
            <!-- Net In Card -->
            <div class="flex flex-col gap-2 rounded-xl bg-surface-dark p-5 border border-border-color shadow-lg hover:border-primary/50 transition-colors group">
              <div class="flex justify-between items-start">
                <p class="text-slate-400 text-sm font-medium uppercase tracking-wider">Net In</p>
                <span class="text-2xl opacity-50 group-hover:opacity-100 transition-opacity">⬇️</span>
              </div>
              <div class="flex items-end gap-3 mt-2">
                <p class="text-white text-3xl font-bold leading-none tracking-tight">{{ netInMbps }} <span class="text-lg text-slate-500">MB/s</span></p>
                <p class="text-green-500 text-sm font-medium flex items-center mb-1">
                  <span class="text-[16px]">↑</span> 12%
                </p>
              </div>
              <div class="w-full bg-slate-800 h-1 mt-2 rounded-full overflow-hidden">
                <div class="bg-green-400 h-full w-[65%] shadow-[0_0_8px_#4ade80]"></div>
              </div>
            </div>
            
            <!-- Net Out Card -->
            <div class="flex flex-col gap-2 rounded-xl bg-surface-dark p-5 border border-border-color shadow-lg hover:border-primary/50 transition-colors group">
              <div class="flex justify-between items-start">
                <p class="text-slate-400 text-sm font-medium uppercase tracking-wider">Net Out</p>
                <span class="text-2xl opacity-50 group-hover:opacity-100 transition-opacity">⬆️</span>
              </div>
              <div class="flex items-end gap-3 mt-2">
                <p class="text-white text-3xl font-bold leading-none tracking-tight">{{ netOutMbps }} <span class="text-lg text-slate-500">GB/s</span></p>
                <p class="text-orange-500 text-sm font-medium flex items-center mb-1">
                  <span class="text-[16px]">↓</span> 5%
                </p>
              </div>
              <div class="w-full bg-slate-800 h-1 mt-2 rounded-full overflow-hidden">
                <div class="bg-orange-500 h-full w-[80%] shadow-[0_0_8px_#f97316]"></div>
              </div>
            </div>
          </div>
          
          <!-- Charts Section -->
          <div class="grid grid-cols-1 xl:grid-cols-2 gap-6 mb-6">
            <div class="flex flex-col gap-4 rounded-xl bg-surface-dark p-6 border border-border-color shadow-lg">
              <div class="flex justify-between items-center">
                <div>
                  <p class="text-slate-400 text-sm font-medium uppercase tracking-wider">Latency (Last 1hr)</p>
                  <p class="text-white text-2xl font-bold mt-1">{{ avgLatency }}ms <span class="text-sm font-normal text-slate-500">avg</span></p>
                </div>
                <div class="flex gap-2">
                  <span class="w-3 h-3 rounded-full bg-primary shadow-[0_0_8px_#25d1f4]"></span>
                  <span class="text-xs text-slate-400">Cluster A</span>
                </div>
              </div>
              <div id="latency-chart" class="relative h-[200px] w-full"></div>
            </div>
            
            <div class="flex flex-col gap-4 rounded-xl bg-surface-dark p-6 border border-border-color shadow-lg">
              <div class="flex justify-between items-center">
                <div>
                  <p class="text-slate-400 text-sm font-medium uppercase tracking-wider">Throughput (RPS)</p>
                  <p class="text-white text-2xl font-bold mt-1">{{ throughput }} <span class="text-sm font-normal text-slate-500">rps</span></p>
                </div>
                <div class="flex gap-4">
                  <div class="flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-primary"></span>
                    <span class="text-xs text-slate-400">HTTP</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-purple-500"></span>
                    <span class="text-xs text-slate-400">gRPC</span>
                  </div>
                </div>
              </div>
              <div id="throughput-chart" class="relative h-[200px] w-full"></div>
            </div>
          </div>
          
          <!-- Server Detail Panel -->
          <div class="flex flex-col rounded-xl border border-border-color bg-surface-dark shadow-2xl overflow-hidden">
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
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <!-- CPU Usage -->
                <div class="bg-background-dark border border-border-color rounded-lg p-4">
                  <div class="flex items-center justify-between mb-2">
                    <span class="text-xs text-slate-400 uppercase tracking-wider">CPU Usage</span>
                    <span class="text-xl">⚡</span>
                  </div>
                  <div class="text-2xl font-bold text-white mb-2">{{ selectedServerMetrics.cpu }}%</div>
                  <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                    <div class="bg-primary h-full transition-all shadow-[0_0_8px_#25d1f4]" :style="`width: ${selectedServerMetrics.cpu}%`"></div>
                  </div>
                  <div class="text-xs text-slate-500 mt-2">{{ selectedServerMetrics.cpuCores }} cores</div>
                </div>

                <!-- Memory Usage -->
                <div class="bg-background-dark border border-border-color rounded-lg p-4">
                  <div class="flex items-center justify-between mb-2">
                    <span class="text-xs text-slate-400 uppercase tracking-wider">Memory</span>
                    <span class="text-xl">💾</span>
                  </div>
                  <div class="text-2xl font-bold text-white mb-2">{{ selectedServerMetrics.memoryUsed }} GB</div>
                  <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                    <div class="bg-purple-500 h-full transition-all shadow-[0_0_8px_#a855f7]" :style="`width: ${selectedServerMetrics.memoryPercent}%`"></div>
                  </div>
                  <div class="text-xs text-slate-500 mt-2">{{ selectedServerMetrics.memoryTotal }} GB total</div>
                </div>

                <!-- Disk Usage -->
                <div class="bg-background-dark border border-border-color rounded-lg p-4">
                  <div class="flex items-center justify-between mb-2">
                    <span class="text-xs text-slate-400 uppercase tracking-wider">Disk</span>
                    <span class="text-xl">💿</span>
                  </div>
                  <div class="text-2xl font-bold text-white mb-2">{{ selectedServerMetrics.diskUsed }} GB</div>
                  <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                    <div class="bg-orange-500 h-full transition-all shadow-[0_0_8px_#f97316]" :style="`width: ${selectedServerMetrics.diskPercent}%`"></div>
                  </div>
                  <div class="text-xs text-slate-500 mt-2">{{ selectedServerMetrics.diskTotal }} GB total</div>
                </div>

                <!-- Temperature -->
                <div class="bg-background-dark border border-border-color rounded-lg p-4">
                  <div class="flex items-center justify-between mb-2">
                    <span class="text-xs text-slate-400 uppercase tracking-wider">Temperature</span>
                    <span class="text-xl">🌡️</span>
                  </div>
                  <div class="text-2xl font-bold text-white mb-2">{{ selectedServer.temp }}°C</div>
                  <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                    <div :class="getTempBarClass(selectedServer.temp)" class="h-full transition-all" :style="`width: ${Math.min(selectedServer.temp * 2, 100)}%`"></div>
                  </div>
                  <div class="text-xs text-slate-500 mt-2">{{ getTempStatus(selectedServer.temp) }}</div>
                </div>
              </div>

              <!-- Network Stats -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                <div class="bg-background-dark border border-border-color rounded-lg p-4">
                  <div class="flex items-center justify-between mb-3">
                    <span class="text-sm text-slate-400 uppercase tracking-wider font-bold">Network I/O</span>
                    <span class="text-xl">📡</span>
                  </div>
                  <div class="space-y-3">
                    <div>
                      <div class="flex justify-between text-xs mb-1">
                        <span class="text-slate-500">Inbound</span>
                        <span class="text-green-400 font-mono">{{ selectedServerMetrics.netIn }} MB/s</span>
                      </div>
                      <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                        <div class="bg-green-400 h-full" :style="`width: ${Math.min(selectedServerMetrics.netIn * 10, 100)}%`"></div>
                      </div>
                    </div>
                    <div>
                      <div class="flex justify-between text-xs mb-1">
                        <span class="text-slate-500">Outbound</span>
                        <span class="text-blue-400 font-mono">{{ selectedServerMetrics.netOut }} MB/s</span>
                      </div>
                      <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                        <div class="bg-blue-400 h-full" :style="`width: ${Math.min(selectedServerMetrics.netOut * 10, 100)}%`"></div>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="bg-background-dark border border-border-color rounded-lg p-4">
                  <div class="flex items-center justify-between mb-3">
                    <span class="text-sm text-slate-400 uppercase tracking-wider font-bold">System Info</span>
                    <span class="text-xl">ℹ️</span>
                  </div>
                  <div class="space-y-2 text-sm">
                    <div class="flex justify-between">
                      <span class="text-slate-500">OS:</span>
                      <span class="text-white font-mono">{{ selectedServer.os }}</span>
                    </div>
                    <div class="flex justify-between">
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
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import axios from 'axios'
import * as echarts from 'echarts/core'
import { LineChart, BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import EditServerModal from '../components/EditServerModal.vue'

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
  logRetention?: number
}

echarts.use([LineChart, BarChart, GridComponent, TooltipComponent, CanvasRenderer])

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
const selectedServer = ref<Server | null>(null)
// removed duplicate selectedServerMetrics ref
const isEditModalOpen = ref(false)
const editingServer = ref<Server | null>(null)

// --- Charts ---
let latencyChart: echarts.ECharts | null = null
let throughputChart: echarts.ECharts | null = null
let updateInterval: number | null = null

// --- Computed ---
// Removed old rack grouping and search functionality since servers are now in sidebar

// Selected server metrics (mock data for now, will be replaced with real API data)
const selectedServerMetrics = computed(() => {
  if (!selectedServer.value) return null
  
  // Mock data - in production this would come from API
  return {
    cpu: Math.floor(Math.random() * 100),
    cpuCores: 8,
    memoryUsed: 12.4,
    memoryTotal: 32,
    memoryPercent: 38,
    diskUsed: 450,
    diskTotal: 1000,
    diskPercent: 45,
    netIn: 45.3,
    netOut: 12.8,
    uptime: '15d 4h 23m',
    processes: 342
  }
})

// Click handler for selecting server
function selectServer(server: Server) {
  selectedServer.value = server
}

// Status badge styling
function getStatusBadgeClass(status: string): string {
  if (status === 'online') return 'bg-green-500/20 text-green-400 border border-green-500/30'
  if (status === 'warning') return 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30'
  return 'bg-red-500/20 text-red-400 border border-red-500/30'
}

// Temperature bar color
function getTempBarClass(temp: number): string {
  if (temp < 40) return 'bg-green-500 shadow-[0_0_8px_#22c55e]'
  if (temp < 60) return 'bg-yellow-500 shadow-[0_0_8px_#eab308]'
  return 'bg-red-500 shadow-[0_0_8px_#ef4444]'
}

// --- Edit Server Logic ---
function handleEditServer(server: Server) {
  editingServer.value = server
  isEditModalOpen.value = true
}

async function handleSaveServer(updatedServer: any) {
  try {
    // 1. Update Hostname
    if (updatedServer.hostname !== editingServer.value?.hostname) {
      await axios.put(`${API_BASE}/agents/${updatedServer.id}/hostname`, {
        hostname: updatedServer.hostname
      })
    }

    // 2. Update Metadata (Rack & Retention)
    await axios.put(`${API_BASE}/agents/${updatedServer.id}/metadata`, {
      rack_location: updatedServer.rack,
      temperature: editingServer.value?.temp || 0, // Keep existing temp
      log_retention_days: updatedServer.logRetention
    })

    // 3. Refresh List
    isEditModalOpen.value = false
    await fetchServers()
    
    // Update selected server if it was the one edited
    if (selectedServer.value?.id === updatedServer.id) {
      selectedServer.value = { ...selectedServer.value, ...updatedServer }
    }

  } catch (e) {
    console.error("Failed to update server", e)
    alert("Failed to update server settings")
  }
}

// Temperature status text
function getTempStatus(temp: number): string {
  if (temp < 40) return 'Normal'
  if (temp < 60) return 'Elevated'
  return 'High - Check Cooling'
}

// Sidebar-specific computed and helpers
const sidebarServers = computed(() => {
  return servers.value.slice(0, 12) // Show max 12 servers in sidebar
})

const totalCapacity = computed(() => {
  if (servers.value.length === 0) return 0
  const total = servers.value.length
  const online = servers.value.filter(s => s.status === 'online').length
  return Math.round((online / total) * 100)
})

function getStatusIcon(status: string): string {
  if (status === 'online') return '●'
  if (status === 'warning') return '⚠'
  return '●' // offline/error
}

function getStatusIconClass(status: string): string {
  if (status === 'online') return 'text-green-500 group-hover:drop-shadow-[0_0_5px_#22c55e]'
  if (status === 'warning') return 'text-yellow-500 animate-pulse'
  return 'text-red-500 animate-pulse' // offline/error
}

function getServerCardClass(status: string): string {
  if (status === 'online') {
    return 'border border-border-color bg-background-dark hover:border-primary/30'
  }
  if (status === 'warning') {
    return 'border border-yellow-500/30 bg-yellow-500/5 hover:border-yellow-500/50'
  }
  return 'border border-red-500/30 bg-red-500/5 hover:border-red-500/50' // offline/error
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
        os: agent.os,
        logRetention: agent.log_retention_days
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
