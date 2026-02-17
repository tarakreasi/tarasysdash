
import axios, { type AxiosInstance } from 'axios';
import type { Agent, Metric, AgentMetadataUpdate, AgentHostnameUpdate, GlobalMetric } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080/api/v1';

class ApiService {
    private client: AxiosInstance;

    constructor() {
        this.client = axios.create({
            baseURL: API_BASE_URL,
            timeout: 10000,
            headers: {
                'Content-Type': 'application/json',
            },
        });
    }

    // --- Agents ---
    async getAgents(): Promise<Agent[]> {
        const response = await this.client.get<Agent[]>('/agents');
        return response.data;
    }

    async updateHostname(agentId: string, hostname: string): Promise<Agent> {
        const payload: AgentHostnameUpdate = { hostname };
        const response = await this.client.put<Agent>(`/agents/${agentId}/hostname`, payload);
        return response.data;
    }

    async updateMetadata(agentId: string, metadata: AgentMetadataUpdate): Promise<Agent> {
        const response = await this.client.put<Agent>(`/agents/${agentId}/metadata`, metadata);
        return response.data;
    }

    // --- Metrics ---
    async getMetrics(agentId: string, limit: number = 10): Promise<Metric[]> {
        const response = await this.client.get<Metric[]>(`/metrics/${agentId}`, {
            params: { limit }
        });
        return response.data;
    }

    async getGlobalHistory(limit: number = 60): Promise<GlobalMetric[]> {
        const response = await this.client.get<GlobalMetric[]>('/metrics/global/history', {
            params: { limit }
        });
        return response.data;
    }
}

export const api = new ApiService();
