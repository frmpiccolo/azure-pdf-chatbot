import type { FileInfo } from '../types/FileInfo'

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000'

export async function uploadFile(file: File): Promise<void> {
  const formData = new FormData()
  formData.append('file', file)

  try {
    const res = await fetch(`${API_URL}/upload/`, {
      method: 'POST',
      body: formData,
    })

    if (!res.ok) throw new Error('Upload failed')
  } catch (error) {
    console.error('Error uploading file:', error)
    throw new Error('Upload failed. Please try again later.')
  }
}

export async function getIndexStatus(): Promise<string> {
  try {
    const res = await fetch(`${API_URL}/status`)
    if (!res.ok) throw new Error('Status not available')

    const data = await res.json()
    return data.status || 'Unknown'
  } catch (error) {
    console.error('Error fetching index status:', error)
    return 'Unavailable'
  }
}

export async function askQuestion(question: string): Promise<string> {
  try {
    const res = await fetch(`${API_URL}/chat/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question }),
    })

    if (!res.ok) throw new Error('Chat API error')

    const data = await res.json()
    return data.answer || 'No answer returned.'
  } catch (error) {
    console.error('Error asking question:', error)
    return 'Sorry, an error occurred while getting the answer.'
  }
}

export async function listFiles(): Promise<FileInfo[]> {
  try {
    const res = await fetch(`${API_URL}/files/`)
    if (!res.ok) throw new Error('API not ready')

    const data = await res.json()
    return data
  } catch (error) {
    console.warn('Using mock files due to error:', error)

    // ✅ Mock fallback for development
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
