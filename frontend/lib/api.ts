// src/lib/api.ts
const API_BASE_URL = "http://127.0.0.1:8000";

export interface Source {
  id: number;
  title: string;
  url: string;
}

export interface SearchResponse {
  mode: string;
  answer: string;
  sources: Source[];
}

export async function askAI(query: string, mode: 'normal' | 'advanced'): Promise<SearchResponse> {
  const res = await fetch(`${API_BASE_URL}/chat/${mode}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });

  if (!res.ok) throw new Error("Backend is not responding");
  return res.json();
}