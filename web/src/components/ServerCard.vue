<template>
  <div 
    class="bg-surface-dark border rounded-lg p-3 hover:bg-background-dark/50 cursor-pointer transition relative group"
    :class="[
      statusColorBorder, 
      isSelected ? 'ring-2 ring-primary' : ''
    ]"
    @click="$emit('click')"
  >
    <!-- Header: Hostname + Status -->
    <div class="flex items-center justify-between mb-2">
      <div class="flex items-center gap-2 min-w-0">
        <div class="size-2.5 rounded-full shadow-glow" :class="statusColorBg"></div>
        <h3 class="font-bold text-sm truncate text-white" :title="server.name">
          {{ server.name }}
        </h3>
      </div>
      <!-- OS Icon -->
      <span class="text-xs" :title="server.os || 'Unknown OS'">
        {{ getOsIcon(server.os) }}
      </span>
    </div>

    <!-- Body: IP & Metrics -->
    <div class="space-y-1">
      <div class="flex items-center justify-between text-xs text-slate-400">
        <span class="font-mono">{{ server.ip || '0.0.0.0' }}</span>
        <span :class="getTempColor(server.temp)">{{ server.temp }}°C</span>
      </div>
    </div>

    <!-- Footer: Rack Location -->
    <div class="mt-2 pt-2 border-t border-border-color flex items-center justify-between group/footer">
      <span class="text-[10px] uppercase tracking-wider text-slate-500 font-semibold">{{ server.rack || 'UNASSIGNED' }}</span>
      
      <div class="flex items-center gap-2">
        <button 
          @click.stop="$emit('edit', server)"
          class="text-slate-500 hover:text-primary opacity-0 group-hover:opacity-100 transition-opacity p-1"
          title="Edit Server"
        >
          ✏️
        </button>
        <span v-if="server.status === 'offline'" class="text-[10px] text-red-500 font-bold">OFFLINE</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  server: {
    id: string
    name: string
    ip: string
    os: string
    rack: string
    temp: number
    status: string
  }
  isSelected?: boolean
}>()

defineEmits(['click', 'edit'])

const statusColorBg = computed(() => {
  switch (props.server.status) {
    case 'online': return 'bg-green-500 shadow-green-500/50'
    case 'warning': return 'bg-yellow-500 shadow-yellow-500/50'
    case 'offline': return 'bg-red-500 shadow-red-500/50'
    default: return 'bg-slate-500'
  }
})

const statusColorBorder = computed(() => {
  switch (props.server.status) {
    case 'online': return 'border-border-color hover:border-green-500/50'
    case 'warning': return 'border-yellow-900/50 hover:border-yellow-500/50'
    case 'offline': return 'border-red-900/50 hover:border-red-500/50'
    default: return 'border-border-color'
  }
})

function getOsIcon(os: string) {
  if (!os) return '❓'
  const lower = os.toLowerCase()
  if (lower.includes('windows')) return '🪟'
  if (lower.includes('linux') || lower.includes('ubuntu') || lower.includes('debian')) return '🐧'
  if (lower.includes('mac') || lower.includes('darwin')) return '🍎'
  return '🖥️'
}

function getTempColor(temp: number) {
  if (temp >= 80) return 'text-red-500 font-bold'
  if (temp >= 60) return 'text-yellow-500'
  return 'text-blue-400'
}
</script>

<style scoped>
.shadow-glow {
  box-shadow: 0 0 8px var(--tw-shadow-color);
}
</style>
