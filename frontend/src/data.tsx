export type ProjectData = {
  ID: string;
  NAME: string;
  DATES: string;
  DESCRIPTION: string;
  USER_ID: string;
};

type ProjectListResponse = {
  projects: ProjectData[];
};

type CreateProjectInput = {
  NAME: string;
  DATES: string;
  DESCRIPTION: string;
  USER_ID?: string;
};

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000';
const PROJECTS_ENDPOINT = `${API_BASE_URL}/api/projects`;

async function ensureJson<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || 'API request failed');
  }

  return response.json() as Promise<T>;
}

export async function fetchData(search = ''): Promise<ProjectData[]> {
  const query = search.trim();
  const endpoint = query
    ? `${PROJECTS_ENDPOINT}?search=${encodeURIComponent(query)}`
    : PROJECTS_ENDPOINT;

  const response = await fetch(endpoint, {
    method: 'GET',
    credentials: 'include',
    headers: {
      Accept: 'application/json',
    },
  });

  const payload = await ensureJson<ProjectListResponse>(response);
  return payload.projects;
}

export async function createProject(input: CreateProjectInput): Promise<ProjectData> {
  const response = await fetch(PROJECTS_ENDPOINT, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    body: JSON.stringify({
      NAME: input.NAME,
      DATES: input.DATES,
      DESCRIPTION: input.DESCRIPTION,
      USER_ID: input.USER_ID ?? '1',
    }),
  });

  return ensureJson<ProjectData>(response);
}
