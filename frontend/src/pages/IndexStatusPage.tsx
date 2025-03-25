import { useEffect, useState } from 'react'
import { getIndexStatus } from '../services/api'

export default function IndexStatusPage() {
  const [status, setStatus] = useState<string>('Loading...')

  useEffect(() => {
    getIndexStatus()
      .then(setStatus)
      .catch(() => setStatus('Error fetching status'))
  }, [])

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Index Status</h1>
      <div className="p-4 bg-base-100 rounded shadow text-lg">{status}</div>
    </div>
  )
}
