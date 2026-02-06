import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Skill {
  id: string;
  name: string;
  description: string;
  complexity: 'SIMPLE' | 'COMPLEX';
  version: string;
  source_url: string;
  last_synced: string;
  created_at: string;
}

export interface ReACTStep {
  thought: string;
  action?: string;
  observation?: string;
}

export interface ExecutionLog {
  id: string;
  skill_id?: string;
  query: string;
  confidence_score?: number;
  steps: ReACTStep[];
  outcome: 'SUCCESS' | 'FAILURE' | 'NO_MATCH';
  model_used?: string;
  duration: number;
  timestamp: string;
}

export const skillApi = {
  listSkills: () => apiClient.get<Skill[]>('/skills'),
  getSkill: (id: string) => apiClient.get<Skill>(`/skills/${id}`),
  registerSkill: (url: string) => apiClient.post<Skill>(`/skills/register?url=${encodeURIComponent(url)}`),
  syncSkill: (id: string) => apiClient.post<Skill>(`/skills/${id}/sync`),
  deleteSkill: (id: string) => apiClient.delete(`/skills/${id}`),
  executeSkill: (query: string) => apiClient.post<ExecutionLog>('/skills/execute', { query }),
};

export default apiClient;
