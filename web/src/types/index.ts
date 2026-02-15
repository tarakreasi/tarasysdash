
export interface Agent {
    id: string;
    hostname: string;
    ip_address: string;
    os: string;
    status: 'online' | 'offline' | 'warning';
    rack_location: string;
    temperature?: number;
    log_retention_days?: number;
    last_seen?: string;
    // mapped from API response
    name?: string; // often hostname is used as name in UI
    rack?: string; // alias for rack_location
    temp?: number; // alias for temperature
    logRetention?: number; // alias for log_retention_days
    ip?: string; // alias for ip_address
}

export interface Metric {
    timestamp: number;
    cpu_usage_percent: number;
    memory_used_bytes: number;
    memory_total_bytes: number;
    disk_usage: DiskUsage[];
    bytes_in: number;
    bytes_out: number;
    uptime_seconds: number;
    process_count: number;
    services: ServiceStatus[];
    temperature?: number;
    // Computed/Derived properties for UI
    cpu?: string;
    memoryUsed?: string;
    memoryTotal?: string;
    diskUsed?: string;
    diskTotal?: string;
    netInDisplay?: string;
    netOutDisplay?: string;
    uptime?: string;
    processes?: number;
    tempDisplay?: number;
}

export interface DiskUsage {
    mount_point: string;
    used_bytes: number;
    total_bytes: number;
}

export interface ServiceStatus {
    name: string;
    running: boolean;
}

export interface AgentMetadataUpdate {
    rack_location: string;
    temperature: number;
    log_retention_days?: number;
}

export interface AgentHostnameUpdate {
    hostname: string;
}
