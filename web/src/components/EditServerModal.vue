<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
    <div class="bg-surface-dark border border-border-color rounded-xl shadow-2xl w-full max-w-md overflow-hidden animate-fade-in">
      
      <!-- Header -->
      <div class="px-6 py-4 border-b border-border-color bg-surface-dark/50 flex justify-between items-center">
        <h3 class="text-lg font-bold text-white flex items-center gap-2">
          <span class="text-primary">✏️</span> Edit Server
        </h3>
        <button @click="close" class="text-slate-400 hover:text-white transition-colors">✕</button>
      </div>

      <!-- Body -->
      <div class="p-6 space-y-4">
        <!-- Hostname -->
        <div>
          <label class="block text-xs font-bold uppercase text-slate-400 mb-1">Hostname</label>
          <input 
            v-model="form.hostname" 
            type="text" 
            class="w-full bg-background-dark border border-border-color rounded p-2 text-white focus:border-primary focus:outline-none transition-colors"
            placeholder="Server Hostname"
          >
        </div>

        <!-- Rack Location -->
        <div>
          <label class="block text-xs font-bold uppercase text-slate-400 mb-1">Rack Location</label>
          <input 
            v-model="form.rack" 
            type="text" 
            class="w-full bg-background-dark border border-border-color rounded p-2 text-white focus:border-primary focus:outline-none transition-colors"
            placeholder="e.g. Rack A1"
          >
        </div>

        <!-- Log Retention -->
        <div>
          <label class="block text-xs font-bold uppercase text-slate-400 mb-1">Log Retention (Days)</label>
          <input 
            v-model.number="form.logRetention" 
            type="number" 
            min="1"
            class="w-full bg-background-dark border border-border-color rounded p-2 text-white focus:border-primary focus:outline-none transition-colors"
            placeholder="30"
          >
          <p class="text-[10px] text-slate-500 mt-1">Metrics older than this will be automatically deleted.</p>
        </div>
      </div>

      <!-- Footer -->
      <div class="px-6 py-4 border-t border-border-color bg-surface-dark/50 flex justify-end gap-3">
        <button @click="close" class="px-4 py-2 rounded text-slate-300 hover:text-white hover:bg-slate-800 transition-colors text-sm font-medium">Cancel</button>
        <button 
          @click="save" 
          :disabled="isSaving"
          class="px-4 py-2 rounded bg-primary text-black font-bold hover:bg-primary-hover transition-colors text-sm disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
        >
          <span v-if="isSaving" class="animate-spin">⏳</span>
          Save Changes
        </button>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import type { Agent } from '../types'

const props = defineProps<{
  isOpen: boolean
  server: Agent | null
}>()

const emit = defineEmits(['close', 'save'])

const form = ref({
  hostname: '',
  rack: '',
  logRetention: 30
})

const isSaving = ref(false)

watch(() => props.server, (newVal) => {
  if (newVal) {
    form.value = {
      hostname: newVal.hostname,
      rack: newVal.rack || '',
      logRetention: newVal.logRetention || 30
    }
  }
}, { immediate: true })

function close() {
  emit('close')
}

async function save() {
  isSaving.value = true
  if (props.server) {
      // Emit save event with form data merged into base server object
      // Note: We emit a merged object that looks like Agent but with updated values
      emit('save', {
        ...props.server,
        hostname: form.value.hostname,
        rack: form.value.rack,
        logRetention: form.value.logRetention
      })
  }
  isSaving.value = false
}
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.2s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
</style>
