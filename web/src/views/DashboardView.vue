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
               <div v-if="sidebarServers.length > 0" class="hidden lg:flex items-center gap-2 px-2 py-0.5 bg-black/30 rounded border border-white/10">
                <span class="w-1.5 h-1.5 bg-green-500 rounded-full shadow-[0_0_5px_#22c55e]"></span>
                <span class="text-[10px] text-slate-300 font-mono">{{ sidebarServers.length }} AGENTS</span>
              </div>
              <div v-else class="hidden lg:flex items-center gap-2 px-2 py-0.5 bg-black/30 rounded border border-white/10">
                <span class="w-1.5 h-1.5 bg-slate-500 rounded-full"></span>
                <span class="text-[10px] text-slate-300 font-mono">NO AGENTS</span>
              </div>
              <span class="text-primary font-mono text-xs">UPDATED: <span class="text-white">{{ lastUpdate || 'NOW' }}</span></span>
            </div>
          </div>
          
          <!-- Content Scroll Area -->
          <div class="flex-1 overflow-y-auto pr-2 scroll-smooth">
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
                :percent="0" 
                variant="purple" 
              />
              
              <MetricCard 
                title="Net In" 
                icon="⬇️" 
                :value="netInMbps" 
                unit="MB/s" 
                :trend="0" 
                :percent="0" 
                variant="green" 
              />
              
              <MetricCard 
                title="Net Out" 
                icon="⬆️" 
                :value="netOutMbps" 
                unit="GB/s" 
                :trend="0" 
                :percent="0" 
                variant="orange" 
              />
            </div>
            
            <!-- Global Charts Component -->
            <GlobalOverviewCharts 
              :cpu-load="cpuLoad"
              :memory-g-b="memoryGB"
              :history="globalMetricsHistory"
            />
            
            <!-- Server Detail Panel Component -->
            <ServerDetailPanel 
              :selected-server="selectedServer"
              :metrics="selectedServerMetrics"
            />
          </div>
        </div>
      </main>
      
      <!-- Right Sidebar Component -->
      <RackSidebar 
        :servers="sidebarServers"
        :selected-server-id="selectedServer?.id"
        :total-capacity="totalCapacity"
        @select="selectServer"
        @edit="handleEditServer"
      />
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
import { onMounted, onUnmounted } from 'vue'
import EditServerModal from '../components/EditServerModal.vue'
import MetricCard from '../components/MetricCard.vue'
import GlobalOverviewCharts from '../components/GlobalOverviewCharts.vue'
import ServerDetailPanel from '../components/ServerDetailPanel.vue'
import RackSidebar from '../components/RackSidebar.vue'
import { useDashboard } from '../composables/useDashboard'

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
  handleSaveServer,
  globalMetricsHistory,
  fetchGlobalHistory
} = useDashboard()

let updateInterval: number | null = null

// --- Lifecycle ---
onMounted(async () => {
  await fetchServers()
  await fetchMetrics() // Initial fetch
  await fetchGlobalHistory()
  
  // Auto-select first server if none selected
  if (sidebarServers.value.length > 0 && !selectedServer.value && sidebarServers.value[0]) {
    selectServer(sidebarServers.value[0])
  }

  updateInterval = window.setInterval(async () => {
    await fetchServers()
    await fetchMetrics()
    await fetchGlobalHistory()
    if (selectedServer.value) {
      await fetchAgentMetrics(selectedServer.value.id)
    }
    lastUpdate.value = new Date().toLocaleTimeString()
  }, 2000)
})

onUnmounted(() => {
  if (updateInterval) clearInterval(updateInterval)
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
