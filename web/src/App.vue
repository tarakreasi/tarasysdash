<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import * as echarts from 'echarts/core'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

echarts.use([LineChart, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer])

const API_BASE = 'http://localhost:8080/api/v1'

interface Agent {
  id: string
  hostname: string
  ip_address: string
  os: string
  created_at: string
  updated_at: string
}

interface Metric {
  timestamp: number
  cpu_usage_percent: number
  memory_used_bytes: number
  memory_total_bytes: number
  disk_free_percent: number
}

const agents = ref<Agent[]>([])
const selectedAgentId = ref<string | null>(null)
const metrics = ref<Metric[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

const latestMetric = computed(() => {
  if (metrics.value.length === 0) return null
  return metrics.value[metrics.value.length - 1]
})

const memoryUsagePercent = computed(() => {
  if (!latestMetric.value) return 0
  return ((latestMetric.value.memory_used_bytes / latestMetric.value.memory_total_bytes) * 100).toFixed(1)
})

function formatBytes(bytes: number): string {
  if (bytes < 1024) return bytes + ' B'
  else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB'
  else if (bytes < 1073741824) return (bytes / 1048576).toFixed(1) + ' MB'
  return (bytes / 1073741824).toFixed(2) + ' GB'
}

async function fetchAgents() {
  try {
    error.value = null
    const response = await axios.get<Agent[]>(`${API_BASE}/agents`)
    agents.value = response.data || []
    if (agents.value.length > 0 && !selectedAgentId.value) {
      selectedAgentId.value = agents.value[0].id
      await fetchMetrics()
    }
    loading.value = false
  } catch (err) {
    error.value = 'Failed to fetch agents'
    console.error('Failed to fetch agents:', err)
    loading.value = false
  }
}

async function fetchMetrics() {
  if (!selectedAgentId.value) return
  try {
    const response = await axios.get<Metric[]>(`${API_BASE}/metrics/${selectedAgentId.value}`)
    metrics.value = (response.data || []).reverse()
    renderChart()
  } catch (err) {
    console.error('Failed to fetch metrics:', err)
  }
}

let chartInstance: echarts.ECharts | null = null

function renderChart() {
  const chartDom = document.getElementById('metrics-chart')
  if (!chartDom) return
  
  if (!chartInstance) {
    chartInstance = echarts.init(chartDom)
  }

  const timestamps = metrics.value.map(m => new Date(m.timestamp * 1000).toLocaleTimeString())
  const cpuData = metrics.value.map(m => m.cpu_usage_percent.toFixed(1))
  const memData = metrics.value.map(m => ((m.memory_used_bytes / m.memory_total_bytes) * 100).toFixed(1))
  const diskData = metrics.value.map(m => m.disk_free_percent.toFixed(1))

  const option: echarts.EChartsOption = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(0, 0, 0, 0.9)',
      borderColor: 'rgba(67, 233, 255, 0.5)',
      borderWidth: 1,
      textStyle: { color: '#fff', fontSize: 13 },
      axisPointer: {
        type: 'cross',
        lineStyle: { color: 'rgba(67, 233, 255, 0.3)' }
      }
    },
    legend: {
      data: ['CPU %', 'Memory %', 'Disk Free %'],
      textStyle: { color: '#bbb', fontSize: 13 },
      top: 10
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '8%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: timestamps,
      axisLine: { lineStyle: { color: '#444' } },
      axisLabel: { color: '#888', fontSize: 11 }
    },
    yAxis: {
      type: 'value',
      name: 'Usage %',
      nameTextStyle: { color: '#888' },
      axisLine: { lineStyle: { color: '#444' } },
      axisLabel: { color: '#888' },
      splitLine: { lineStyle: { color: '#2a2a2a' } },
      min: 0,
      max: 100
    },
    series: [
      {
        name: 'CPU %',
        type: 'line',
        data: cpuData,
        smooth: true,
        lineStyle: { color: '#43e9ff', width: 2 },
        itemStyle: { color: '#43e9ff' },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(67, 233, 255, 0.3)' },
              { offset: 1, color: 'rgba(67, 233, 255, 0.05)' }
            ]
          }
        }
      },
      {
        name: 'Memory %',
        type: 'line',
        data: memData,
        smooth: true,
        lineStyle: { color: '#ff6b6b', width: 2 },
        itemStyle: { color: '#ff6b6b' },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(255, 107, 107, 0.3)' },
              { offset: 1, color: 'rgba(255, 107, 107, 0.05)' }
            ]
          }
        }
      },
      {
        name: 'Disk Free %',
        type: 'line',
        data: diskData,
        smooth: true,
        lineStyle: { color: '#4caf50', width: 2 },
        itemStyle: { color: '#4caf50' },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(76, 175, 80, 0.3)' },
              { offset: 1, color: 'rgba(76, 175, 80, 0.05)' }
            ]
          }
        }
      }
    ]
  }

  chartInstance.setOption(option)
}

onMounted(async () => {
  await fetchAgents()
  setInterval(fetchAgents, 5000)
  setInterval(fetchMetrics, 3000)
  
  // Handle window resize
  window.addEventListener('resize', () => {
    chartInstance?.resize()
  })
})
</script>

<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <div class="header-content">
        <div>
          <h1>taraSysDash</h1>
          <p>Real-time System Monitoring</p>
        </div>
        <div class="header-stats">
          <span class="stat-badge">{{ agents.length }} Agent{{ agents.length !== 1 ? 's' : '' }}</span>
        </div>
      </div>
    </header>

    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>Loading agents...</p>
    </div>

    <div v-else-if="error" class="error-container">
      <p>{{ error }}</p>
    </div>

    <div v-else class="dashboard-content">
      <aside class="agent-sidebar">
        <h2>Agents</h2>
        <div class="agent-list">
          <div
            v-for="agent in agents"
            :key="agent.id"
            :class="['agent-card', { active: agent.id === selectedAgentId }]"
            @click="selectedAgentId = agent.id; fetchMetrics()"
          >
            <div class="agent-status"></div>
            <div class="agent-info">
              <p class="agent-id">{{ agent.id }}</p>
              <p class="agent-host">{{ agent.hostname }}</p>
              <p class="agent-meta">{{ agent.ip_address || 'N/A' }}</p>
            </div>
          </div>
        </div>
      </aside>

      <main class="metrics-panel">
        <div v-if="latestMetric" class="metric-cards">
          <div class="metric-card cpu">
            <div class="metric-icon">⚡</div>
            <div class="metric-details">
              <p class="metric-label">CPU Usage</p>
              <p class="metric-value">{{ latestMetric.cpu_usage_percent.toFixed(1) }}%</p>
            </div>
          </div>

          <div class="metric-card memory">
            <div class="metric-icon">💾</div>
            <div class="metric-details">
              <p class="metric-label">Memory Usage</p>
              <p class="metric-value">{{ memoryUsagePercent }}%</p>
              <p class="metric-subtext">{{ formatBytes(latestMetric.memory_used_bytes) }} / {{ formatBytes(latestMetric.memory_total_bytes) }}</p>
            </div>
          </div>

          <div class="metric-card disk">
            <div class="metric-icon">💿</div>
            <div class="metric-details">
              <p class="metric-label">Disk Free</p>
              <p class="metric-value">{{ latestMetric.disk_free_percent.toFixed(1) }}%</p>
            </div>
          </div>
        </div>

        <div class="chart-container">
          <h2>Historical Metrics</h2>
          <div id="metrics-chart"></div>
        </div>
      </main>
    </div>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
  color: #e0e0e0;
  min-height: 100vh;
}

.dashboard {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.dashboard-header {
  background: rgba(10, 14, 39, 0.7);
  backdrop-filter: blur(15px);
  border-bottom: 1px solid rgba(67, 233, 255, 0.2);
  padding: 1.5rem 2rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1600px;
  margin: 0 auto;
}

.dashboard-header h1 {
  font-size: 1.8rem;
  font-weight: 700;
  background: linear-gradient(90deg, #43e9ff, #4caf50);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.3rem;
}

.dashboard-header p {
  color: #bbb;
  font-size: 0.9rem;
}

.header-stats {
  display: flex;
  gap: 1rem;
}

.stat-badge {
  background: rgba(67, 233, 255, 0.15);
  border: 1px solid rgba(67, 233, 255, 0.3);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  color: #43e9ff;
  font-weight: 600;
}

.loading-container, .error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  gap: 1rem;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(67, 233, 255, 0.2);
  border-top-color: #43e9ff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.dashboard-content {
  display: flex;
  flex: 1;
  gap: 1.5rem;
  padding: 1.5rem;
  max-width: 1600px;
  margin: 0 auto;
  width: 100%;
}

.agent-sidebar {
  width: 300px;
  background: rgba(26, 31, 58, 0.6);
  backdrop-filter: blur(15px);
  border-radius: 16px;
  border: 1px solid rgba(67, 233, 255, 0.15);
  padding: 1.5rem;
  height: fit-content;
}

.agent-sidebar h2 {
  font-size: 1.2rem;
  margin-bottom: 1.2rem;
  color: #fff;
}

.agent-list {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.agent-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(67, 233, 255, 0.2);
  border-radius: 12px;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: flex-start;
  gap: 0.9rem;
}

.agent-card:hover {
  background: rgba(67, 233, 255, 0.08);
  border-color: rgba(67, 233, 255, 0.4);
  transform: translateY(-2px);
}

.agent-card.active {
  background: rgba(67, 233, 255, 0.12);
  border-color: #43e9ff;
  box-shadow: 0 4px 12px rgba(67, 233, 255, 0.2);
}

.agent-status {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #4caf50;
  box-shadow: 0 0 10px #4caf50;
  animation: pulse 2s ease-in-out infinite;
  margin-top: 4px;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.agent-info {
  flex: 1;
}

.agent-id {
  font-weight: 600;
  color: #fff;
  font-size: 0.95rem;
  margin-bottom: 0.3rem;
}

.agent-host {
  font-size: 0.8rem;
  color: #888;
  margin-bottom: 0.2rem;
}

.agent-meta {
  font-size: 0.75rem;
  color: #666;
}

.metrics-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.metric-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.2rem;
}

.metric-card {
  background: rgba(26, 31, 58, 0.6);
  backdrop-filter: blur(15px);
  border-radius: 16px;
  border: 1px solid rgba(67, 233, 255, 0.15);
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.2rem;
  transition: all 0.2s ease;
}

.metric-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.metric-card.cpu {
  border-color: rgba(67, 233, 255, 0.3);
}

.metric-card.memory {
  border-color: rgba(255, 107, 107, 0.3);
}

.metric-card.disk {
  border-color: rgba(76, 175, 80, 0.3);
}

.metric-icon {
  font-size: 2.5rem;
  opacity: 0.9;
}

.metric-details {
  flex: 1;
}

.metric-label {
  font-size: 0.85rem;
  color: #999;
  margin-bottom: 0.4rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.metric-value {
  font-size: 2rem;
  font-weight: 700;
  color: #fff;
  line-height: 1;
}

.metric-subtext {
  font-size: 0.75rem;
  color: #777;
  margin-top: 0.4rem;
}

.chart-container {
  background: rgba(26, 31, 58, 0.6);
  backdrop-filter: blur(15px);
  border-radius: 16px;
  border: 1px solid rgba(67, 233, 255, 0.15);
  padding: 2rem;
  flex: 1;
}

.chart-container h2 {
  font-size: 1.3rem;
  margin-bottom: 1.5rem;
  color: #fff;
}

#metrics-chart {
  width: 100%;
  height: 450px;
}

@media (max-width: 1200px) {
  .dashboard-content {
    flex-direction: column;
  }

  .agent-sidebar {
    width: 100%;
  }

  .agent-list {
    flex-direction: row;
    overflow-x: auto;
  }

  .agent-card {
    min-width: 200px;
  }
}

@media (max-width: 768px) {
  .metric-cards {
    grid-template-columns: 1fr;
  }

  #metrics-chart {
    height: 350px;
  }
}
</style>
