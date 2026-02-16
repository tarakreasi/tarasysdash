<template>
  <aside class="w-full lg:w-80 border-l border-border-color bg-surface-dark overflow-y-auto hidden lg:flex flex-col">
    <!-- Sidebar Header with Actions -->
    <div class="px-5 py-4 border-b border-border-color bg-surface-dark sticky top-0 z-10 flex flex-col gap-4">
       <!-- Action Buttons -->
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
        v-for="server in servers" 
        :key="server.id"
        :class="[
          getServerCardClass(server.status),
          selectedServerId === server.id ? 'ring-2 ring-primary bg-primary/10' : ''
        ]"
        class="flex gap-3 rounded-lg p-3 items-center transition-all cursor-pointer group"
        @click="$emit('select', server)"
      >
        <span :class="getStatusIconClass(server.status)" class="text-[20px]">{{ getStatusIcon(server.status) }}</span>
        <div class="flex flex-col flex-1 min-w-0">
          <div class="flex items-center justify-between">
            <h2 class="text-white text-sm font-bold leading-tight font-mono truncate">{{ server.hostname }}</h2>
            <button 
              @click.stop="$emit('edit', server)"
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
      <div v-if="servers.length === 0" class="text-center py-8 text-slate-500 text-sm">
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
</template>

<script setup lang="ts">
import { getServerCardClass, getStatusIcon, getStatusIconClass } from '../utils/formatters'
import type { Agent } from '../types'

defineProps<{
  servers: Agent[]
  selectedServerId: string | undefined
  totalCapacity: number
}>()

defineEmits<{
  (e: 'select', server: Agent): void
  (e: 'edit', server: Agent): void
}>()
</script>
