import apiClient from './api';


export interface RepoSkill {
  path: string;
  name: string;
}

export interface ListSkillsResponse {
  skills: RepoSkill[];
}

export interface ListLocalSkillsResponse {
  absolute_path: string;
  skills: (RepoSkill & { has_metadata: boolean })[];
}

export interface GitHubDeepLink {
  is_github: boolean;
  is_deep_link: boolean;
  repo_url: string;
  branch: string | null;
  sub_path: string | null;
}

export interface RiskFinding {
  category: 'PII' | 'MALICIOUS_CODE' | 'DANGEROUS_OP' | 'OTHER';
  detail: string;
  severity: 'HIGH' | 'MEDIUM' | 'LOW';
}

export interface RegistrationQueueItem {
  path: string;
  name: string;
  safety_status: 'SCANNING' | 'SAFE' | 'RISKY' | 'FAILED';
  judgment: 'PENDING' | 'APPROVED' | 'REJECTED';
  risk_findings: RiskFinding[];
  code_content?: string;
  error_message?: string;
}

export interface RegistrationBatch {
  id: string;
  repo_url: string;
  status: 'SCANNING' | 'REVIEW_REQUIRED' | 'COMPLETED' | 'FAILED';
  items: RegistrationQueueItem[];
  created_at: string;
}

export const registrationApi = {
  listRepoSkills: (repoUrl: string) =>
    apiClient.get<ListSkillsResponse>(`/skills/list-from-repo?repo_url=${encodeURIComponent(repoUrl)}`),

  listLocalSkills: (absolutePath: string) =>
    apiClient.get<ListLocalSkillsResponse>(`/skills/list-from-local?absolute_path=${encodeURIComponent(absolutePath)}`),

  parseGitHubUrl: (url: string) =>
    apiClient.get<GitHubDeepLink>(`/skills/parse-github-url?url=${encodeURIComponent(url)}`),

  startBatchScan: (repoUrl: string, selectedPaths: string[]) =>
    apiClient.post<{ batch_id: string }>('/skills/register-batch', {
      repo_url: repoUrl,
      selected_paths: selectedPaths,
    }),

  getBatchStatus: (batchId: string) =>
    apiClient.get<RegistrationBatch>(`/skills/registration-batches/${batchId}`),

  listBatches: () =>
    apiClient.get<RegistrationBatch[]>('/skills/registration-batches'),

  judgeItem: (batchId: string, path: string, judgment: 'APPROVED' | 'REJECTED') =>
    apiClient.post(`/skills/registration-batches/${batchId}/judge`, {
      path,
      judgment,
    }),

  approveAllSafe: (batchId: string) =>
    apiClient.post<{ approved_count: number }>(`/skills/registration-batches/${batchId}/approve-all-safe`),

  getSkillDocumentation: (skillId: string) =>
    apiClient.get<{ skill_id: string; content: string; file_name: string }>(`/skills/${skillId}/documentation`),
};
