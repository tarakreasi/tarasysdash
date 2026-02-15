<template>
  <div 
    class="flex flex-col gap-2 rounded-xl bg-surface-dark/80 backdrop-blur-md p-5 border border-border-color shadow-lg transition-all duration-300 group"
    :class="hoverClasses"
  >
    <div class="flex justify-between items-start">
      <p class="text-slate-400 text-sm font-medium uppercase tracking-wider">{{ title }}</p>
      <span class="text-2xl opacity-50 group-hover:opacity-100 transition-opacity">{{ icon }}</span>
    </div>
    <div class="flex items-end gap-3 mt-2">
      <p class="text-white text-3xl font-bold leading-none tracking-tight">
        {{ value }} <span v-if="unit" class="text-lg text-slate-500">{{ unit }}</span>
      </p>
      
      <!-- Trend -->
      <p v-if="trend !== undefined" class="text-sm font-medium flex items-center mb-1" :class="trend >= 0 ? 'text-green-500' : 'text-orange-500'">
        <span class="text-[16px]">{{ trend >= 0 ? '↑' : '↓' }}</span> {{ Math.abs(trend) }}%
      </p>
      
      <!-- Subtext (e.g. 'stable') -->
      <p v-else-if="subtext" class="text-slate-400 text-sm font-medium mb-1">{{ subtext }}</p>
    </div>
    
    <!-- Progress Bar -->
    <div class="w-full bg-slate-800 h-1 mt-2 rounded-full overflow-hidden">
      <div 
        class="h-full transition-all duration-500" 
        :class="barColorClass"
        :style="`width: ${Math.min(percent, 100)}%`"
      ></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  title: string
  icon: string
  value: string | number
  unit?: string
  trend?: number
  subtext?: string
  percent: number
  variant: 'primary' | 'purple' | 'green' | 'orange'
}>()

const hoverClasses = computed(() => {
  switch (props.variant) {
    case 'primary': return 'hover:border-primary/50 hover:shadow-[0_0_20px_rgba(37,209,244,0.2)]'
    case 'purple': return 'hover:border-purple-500/50 hover:shadow-[0_0_20px_rgba(168,85,247,0.2)]'
    case 'green': return 'hover:border-green-500/50 hover:shadow-[0_0_20px_rgba(74,222,128,0.2)]'
    case 'orange': return 'hover:border-orange-500/50 hover:shadow-[0_0_20px_rgba(249,115,22,0.2)]'
    default: return ''
  }
})

const barColorClass = computed(() => {
  switch (props.variant) {
    case 'primary': return 'bg-primary shadow-[0_0_8px_#25d1f4]'
    case 'purple': return 'bg-purple-500 shadow-[0_0_8px_#a855f7]'
    case 'green': return 'bg-green-400 shadow-[0_0_8px_#4ade80]'
    case 'orange': return 'bg-orange-500 shadow-[0_0_8px_#f97316]'
    default: return 'bg-slate-500'
  }
})
</script>
