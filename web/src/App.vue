<template>
  <div class="min-h-screen bg-background-dark">
    <nav class="flex items-center justify-between border-b border-border-color bg-surface-dark/95 backdrop-blur px-6 py-3">
      <div class="flex items-center gap-4 text-white">
        <div class="size-6 text-primary animate-pulse">
          <svg fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
            <path d="M42.4379 44C42.4379 44 36.0744 33.9038 41.1692 24C46.8624 12.9336 42.2078 4 42.2078 4L7.01134 4C7.01134 4 11.6577 12.932 5.96912 23.9969C0.876273 33.9029 7.27094 44 7.27094 44L42.4379 44Z" fill="currentColor"></path>
          </svg>
        </div>
        <h2 class="text-xl font-bold tracking-wider uppercase">taraSysDash</h2>
      </div>
      
      <div class="flex gap-8">
        <router-link 
          v-for="link in navLinks" 
          :key="link.path"
          :to="link.path"
          class="text-sm text-slate-400 hover:text-primary transition-colors"
          active-class="text-primary"
        >
          {{ link.name }}
        </router-link>
      </div>

      <div class="flex items-center gap-3">
        <span class="text-xs text-green-500 flex items-center gap-2">
          <span class="size-2 bg-green-500 rounded-full animate-pulse"></span>
          SYSTEM ONLINE
        </span>
      </div>
    </nav>
    
    <router-view />
  </div>
</template>

<script setup lang="ts">
const navLinks = [
  { name: 'Dashboard', path: '/' },
  { name: 'Deployments', path: '/deployments' },
  { name: 'Infrastructure', path: '/infrastructure' },
  { name: 'Security', path: '/security' }
]
</script>
