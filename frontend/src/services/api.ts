import type { FileInfo } from '../types/FileInfo'

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000'

export async function uploadFile(file: File): Promise<void> {
  const formData = new FormData()
  formData.append('file', file)

  await fetch(`${API_URL}/upload/`, {
    method: 'POST',
    body: formData,
  })
}

export async function getIndexStatus(): Promise<string> {
  const res = await fetch(`${API_URL}/status`)
  const data = await res.json()
  return data.status || 'Unknown'
}

export async function askQuestion(question: string): Promise<string> {
  const res = await fetch(`${API_URL}/chat/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
  })
  const data = await res.json()
  return data.answer
}

export async function listFiles(): Promise<FileInfo[]> {
  try {
    const res = await fetch(`${API_URL}/files/`)
    if (!res.ok) throw new Error('API not ready')
    const data = await res.json()
    return data
  } catch (error) {
    // Mock de fallback (para desenvolvimento sem backend)
    return [
      {
        filename: 'demo.pdf',
        size: 45678,
        uploadedAt: new Date().toISOString(),
        indexed: true,
      },
      {
        filename: 'report.pdf',
        size: 92345,
        uploadedAt: new Date().toISOString(),
        indexed: false,
      },
    ]
  }
}
