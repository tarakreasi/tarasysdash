<template>
  <div v-if="show" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="closeModal">
    <div class="bg-surface-dark border border-border-color rounded-lg p-6 w-full max-w-md">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-xl font-bold">Server Preferences</h2>
        <button @click="closeModal" class="text-slate-400 hover:text-white">✕</button>
      </div>

      <div class="space-y-4">
        <!-- Hostname -->
        <div>
          <label class="block text-sm text-slate-400 mb-2">Hostname</label>
          <input 
            v-model="editedHostname" 
            type="text" 
            class="w-full bg-background-dark border border-border-color rounded px-3 py-2 text-white focus:outline-none focus:border-primary"
            :disabled="saving"
          />
        </div>

        <!-- Rack Location (readonly for now) -->
        <div>
          <label class="block text-sm text-slate-400 mb-2">Rack Location</label>
          <input 
            :value="server.rack" 
            type="text" 
            class="w-full bg-background-dark/50 border border-border-color rounded px-3 py-2 text-slate-500"
            disabled
          />
        </div>

        <!-- Temperature (readonly) -->
        <div>
          <label class="block text-sm text-slate-400 mb-2">Temperature</label>
          <input 
            :value="`${server.temp}°C`" 
            type="text" 
            class="w-full bg-background-dark/50 border border-border-color rounded px-3 py-2 text-slate-500"
            disabled
          />
        </div>

        <!-- Status -->
        <div>
          <label class="block text-sm text-slate-400 mb-2">Status</label>
          <div class="flex items-center gap-2">
            <div class="size-2 rounded-full" :class="getStatusColor(server.status)"></div>
            <span class="text-sm capitalize">{{ server.status }}</span>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex gap-3 mt-6">
        <button 
          @click="saveChanges" 
          :disabled="saving || editedHostname === server.name"
          class="flex-1 bg-primary hover:bg-primary-dim disabled:bg-slate-700 disabled:text-slate-500 text-white font-medium py-2 px-4 rounded transition"
        >
          {{ saving ? 'Saving...' : 'Save Changes' }}
        </button>
        <button 
          @click="closeModal" 
          class="px-4 py-2 text-slate-400 hover:text-white transition"
        >
          Cancel
        </button>
      </div>

      <!-- Error message -->
      <div v-if="error" class="mt-3 text-sm text-red-500">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import axios from 'axios'

const props = defineProps<{
  server: any
  show: boolean
}>()

const emit = defineEmits<{
  close: []
  updated: []
}>()

const API_BASE = 'http://localhost:8080/api/v1'

const editedHostname = ref('')
const saving = ref(false)
const error = ref('')

watch(() => props.show, (newVal) => {
  if (newVal) {
    editedHostname.value = props.server.name
    error.value = ''
  }
})

function getStatusColor(status: string) {
  if (status === 'online') return 'bg-green-500'
  if (status === 'warning') return 'bg-yellow-500'
  if (status === 'offline') return 'bg-red-500'
  return 'bg-gray-500'
}

function closeModal() {
  emit('close')
}

async function saveChanges() {
  if (editedHostname.value === props.server.name) return
  
  saving.value = true
  error.value = ''
  
  try {
    await axios.put(`${API_BASE}/agents/${props.server.id}/hostname`, {
      hostname: editedHostname.value
    })
    emit('updated')
    emit('close')
  } catch (err: any) {
    error.value = err.response?.data?.error || 'Failed to update hostname'
  } finally {
    saving.value = false
  }
}
</script>
