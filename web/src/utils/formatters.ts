
export function formatUptime(seconds: number): string {
    if (!seconds) return '0s'
    const d = Math.floor(seconds / (3600 * 24))
    const h = Math.floor((seconds % (3600 * 24)) / 3600)
    const m = Math.floor((seconds % 3600) / 60)
    if (d > 0) return `${d}d ${h}h ${m}m`
    if (h > 0) return `${h}h ${m}m`
    return `${m}m`
}

export function getStatusBadgeClass(status: string): string {
    if (status === 'online') return 'bg-green-500/20 text-green-400 border border-green-500/30'
    if (status === 'warning') return 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30'
    return 'bg-red-500/20 text-red-400 border border-red-500/30'
}

export function getStatusIcon(status: string): string {
    if (status === 'online') return '●'
    if (status === 'warning') return '⚠'
    return '●' // offline/error
}

export function getStatusIconClass(status: string): string {
    if (status === 'online') return 'text-green-500 group-hover:drop-shadow-[0_0_5px_#22c55e]'
    if (status === 'warning') return 'text-yellow-500 animate-pulse'
    return 'text-red-500 animate-pulse' // offline/error
}

export function getServerCardClass(status: string): string {
    if (status === 'online') {
        return 'border border-border-color bg-background-dark hover:border-primary/30'
    }
    if (status === 'warning') {
        return 'border border-yellow-500/30 bg-yellow-500/5 hover:border-yellow-500/50'
    }
    return 'border border-red-500/30 bg-red-500/5 hover:border-red-500/50' // offline/error
}
