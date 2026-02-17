<template>
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
    <div v-if="selectedServer && metrics" class="p-6">
      <!-- Visual Gauges Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        <ServerGauge 
          title="CPU Load" 
          :value="parseFloat(metrics.cpu)" 
          variant="cpu" 
        />
        
        <ServerGauge 
          title="Memory" 
          :value="(parseFloat(metrics.memoryUsed) / parseFloat(metrics.memoryTotal)) * 100" 
          unit="GB"
          variant="ram" 
          :detail-formatter="() => `${metrics!.memoryUsed}GB\n${metrics!.memoryTotal}GB`"
        />

        <ServerGauge 
          title="Temperature" 
          :value="metrics.temp" 
          variant="temp" 
          unit="°C"
        />
      </div>

      <!-- Disk, Network, System Info Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Disk Usage Card -->
        <div class="bg-background-dark border border-border-color rounded-lg p-6 flex flex-col">
          <div class="flex items-center justify-between mb-4">
            <span class="text-sm text-slate-400 uppercase tracking-wider font-bold">Disk Usage</span>
            <span class="text-xl">💽</span>
          </div>
          
          <div class="space-y-4 max-h-[160px] overflow-y-auto pr-2 custom-scrollbar">
            <div v-for="disk in metrics.disks" :key="disk.path" class="space-y-1">
              <div class="flex justify-between text-[10px] uppercase font-bold tracking-tight">
                <span class="text-slate-400 truncate w-24" :title="disk.path">{{ disk.path }}</span>
                <span class="text-white">{{ disk.used }} / {{ disk.total }} GB</span>
              </div>
              <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                <div 
                  class="h-full transition-all duration-500 shadow-[0_0_5px_#22c55e]" 
                  :class="disk.percent > 90 ? 'bg-red-500' : disk.percent > 70 ? 'bg-orange-400' : 'bg-green-400'"
                  :style="`width: ${disk.percent}%`"
                ></div>
              </div>
            </div>
          </div>
          <div v-if="!metrics.disks || metrics.disks.length === 0" class="flex-1 flex items-center justify-center text-slate-600 italic text-xs">
            No disks detected
          </div>
        </div>

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
                <span class="text-green-400 font-mono">{{ metrics.netInDisplay }} Mbps</span>
              </div>
              <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                <div class="bg-green-400 h-full" :style="`width: ${Math.min(metrics.netIn * 10, 100)}%`"></div>
              </div>
            </div>
            <div>
              <div class="flex justify-between text-xs mb-1">
                <span class="text-slate-500">Outbound</span>
                <span class="text-blue-400 font-mono">{{ metrics.netOutDisplay }} Mbps</span>
              </div>
              <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                <div class="bg-blue-400 h-full" :style="`width: ${Math.min(metrics.netOut * 10, 100)}%`"></div>
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
              <span class="text-white font-mono">{{ metrics.uptime }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-slate-500">Processes:</span>
              <span class="text-white font-mono">{{ metrics.processes }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Services Status -->
      <div class="bg-background-dark border border-border-color rounded-lg p-4 mt-4" v-if="metrics.services && metrics.services.length > 0">
        <div class="flex items-center justify-between mb-3">
          <span class="text-sm text-slate-400 uppercase tracking-wider font-bold">Services</span>
          <span class="text-xl">⚙️</span>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-sm">
          <div v-for="svc in metrics.services" :key="svc.name" class="flex justify-between items-center bg-slate-800/50 p-2 rounded">
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
</template>

<script setup lang="ts">
import ServerGauge from './ServerGauge.vue'
import { getStatusBadgeClass } from '../utils/formatters'
import type { Agent } from '../types'

defineProps<{
  selectedServer: Agent | null
  metrics: any | null // Use any for computed metrics object for now
}>()
</script>
