import { ref, computed } from 'vue'
import { api } from '../services/api'
import type { Agent, Metric } from '../types'
import { formatUptime } from '../utils/formatters'

export function useDashboard() {
    // --- State ---
    const cpuLoad = ref(0)
    const cpuTrend = ref(0)
    const memoryGB = ref(0)
    const netInMbps = ref(0)
    const netOutMbps = ref(0)
    const lastUpdate = ref('--:--:--')
    const servers = ref<Agent[]>([])
    const selectedServer = ref<Agent | null>(null)
    const selectedServerRawMetrics = ref<Metric[] | null>(null)

    const isEditModalOpen = ref(false)
    const editingServer = ref<Agent | null>(null)

    // --- Computed ---
    const selectedServerMetrics = computed(() => {
        if (!selectedServerRawMetrics.value || selectedServerRawMetrics.value.length === 0) return null

        const m = selectedServerRawMetrics.value[0]!
        if (!m) return null

        const prevM = selectedServerRawMetrics.value.length > 1 ? selectedServerRawMetrics.value[1] : null

        // Calculate disk percent
        const diskUsed = m.disk_usage && m.disk_usage.length > 0 ? (m.disk_usage[0]!.used_bytes / 1073741824) : 0
        const diskTotal = m.disk_usage && m.disk_usage.length > 0 ? (m.disk_usage[0]!.total_bytes / 1073741824) : 1
        const diskPercent = (diskUsed / diskTotal) * 100

        // Calculate Network Rate (MB/s)
        let netInRate = 0
        let netOutRate = 0
        if (prevM) {
            const timeDiff = m.timestamp - prevM.timestamp
            if (timeDiff > 0) {
                netInRate = (m.bytes_in - prevM.bytes_in) / timeDiff / 1024 / 1024
                netOutRate = (m.bytes_out - prevM.bytes_out) / timeDiff / 1024 / 1024
            }
        }

        return {
            cpu: m.cpu_usage_percent.toFixed(1),
            cpuCores: 0,
            memoryUsed: (m.memory_used_bytes / 1073741824).toFixed(1),
            memoryTotal: (m.memory_total_bytes / 1073741824).toFixed(1),
            memoryPercent: Math.round((m.memory_used_bytes / m.memory_total_bytes) * 100),
            diskUsed: diskUsed.toFixed(1),
            diskTotal: diskTotal.toFixed(1),
            diskPercent: Math.round(diskPercent),
            netIn: netInRate,
            netOut: netOutRate,
            netInDisplay: netInRate.toFixed(2),
            netOutDisplay: netOutRate.toFixed(2),
            uptime: formatUptime(m.uptime_seconds),
            processes: m.process_count,
            services: m.services || [],
            temp: m.temperature || 0
        }
    })

    const sidebarServers = computed(() => {
        return servers.value.slice(0, 12) // Show max 12 servers in sidebar
    })

    const totalCapacity = computed(() => {
        if (servers.value.length === 0) return 0
        const total = servers.value.length
        const online = servers.value.filter(s => s.status === 'online').length
        return Math.round((online / total) * 100)
    })

    // --- Actions ---
    async function fetchAgentMetrics(agentId: string) {
        try {
            const metrics = await api.getMetrics(agentId, 2) // Fetch 2 for rate calc
            if (metrics && metrics.length > 0) {
                selectedServerRawMetrics.value = metrics
            } else {
                selectedServerRawMetrics.value = null
            }
        } catch (e) {
            console.error("Failed to fetch agent metrics", e)
            selectedServerRawMetrics.value = null
        }
    }

    function selectServer(server: Agent) {
        selectedServer.value = server
        fetchAgentMetrics(server.id)
    }

    async function fetchServers() {
        try {
            const agents = await api.getAgents()
            if (agents) {
                servers.value = agents.map((agent) => ({
                    ...agent,
                    name: agent.hostname,
                    rack: agent.rack_location || 'Unassigned',
                    temp: agent.temperature || 0,
                    logRetention: agent.log_retention_days
                }))
            }
        } catch (err) {
            console.error('Failed to fetch servers:', err)
        }
    }

    async function fetchMetrics() {
        try {
            if (servers.value.length === 0) return

            let totalCpu = 0
            let totalMem = 0
            let totalNetIn = 0
            let totalNetOut = 0
            let activeCount = 0

            const activeServers = servers.value.filter(s => s.status === 'online')

            if (activeServers.length === 0) {
                cpuLoad.value = 0
                memoryGB.value = 0
                netInMbps.value = 0
                netOutMbps.value = 0
                return
            }

            const promises = activeServers.map(s => api.getMetrics(s.id, 2))
            const results = await Promise.allSettled(promises)

            for (const result of results) {
                if (result.status === 'fulfilled' && result.value && result.value.length > 0) {
                    const m = result.value[0]!
                    const prevM = result.value.length > 1 ? result.value[1] : null

                    totalCpu += m.cpu_usage_percent
                    totalMem += m.memory_used_bytes

                    if (prevM) {
                        const timeDiff = m.timestamp - prevM.timestamp
                        if (timeDiff > 0) {
                            totalNetIn += (m.bytes_in - prevM.bytes_in) / timeDiff
                            totalNetOut += (m.bytes_out - prevM.bytes_out) / timeDiff
                        }
                    }
                    activeCount++
                }
            }

            if (activeCount > 0) {
                cpuLoad.value = parseFloat((totalCpu / activeCount).toFixed(1))
                memoryGB.value = parseFloat((totalMem / 1073741824).toFixed(1))
                netInMbps.value = parseFloat((totalNetIn / 1024 / 1024).toFixed(2))
                netOutMbps.value = parseFloat((totalNetOut / 1024 / 1024).toFixed(2))
                cpuTrend.value = Math.floor(Math.random() * 10) - 5
            }

        } catch (e) { console.error(e) }
    }

    function handleEditServer(server: Agent) {
        editingServer.value = server
        isEditModalOpen.value = true
    }

    async function handleSaveServer(updatedServer: any) {
        try {
            if (!editingServer.value) return;

            if (updatedServer.hostname !== editingServer.value.hostname) {
                await api.updateHostname(updatedServer.id, updatedServer.hostname)
            }

            await api.updateMetadata(updatedServer.id, {
                rack_location: updatedServer.rack,
                temperature: editingServer.value.temp || 0,
                log_retention_days: updatedServer.logRetention
            })

            isEditModalOpen.value = false
            await fetchServers()

            if (selectedServer.value?.id === updatedServer.id) {
                const fresh = servers.value.find(s => s.id === updatedServer.id)
                if (fresh) selectedServer.value = fresh
            }

        } catch (e) {
            console.error("Failed to update server", e)
            alert("Failed to update server settings")
        }
    }

    return {
        // State
        cpuLoad,
        cpuTrend,
        memoryGB,
        netInMbps,
        netOutMbps,
        lastUpdate,
        servers,
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
        handleSaveServer
    }
}
