import { useEffect, useState } from 'react'
import { getIndexStatus } from '../services/api'

export default function IndexStatusPage() {
  const [status, setStatus] = useState<string>('Loading...')
  const [error, setError] = useState(false)

  useEffect(() => {
    getIndexStatus()
      .then((s) => {
        setStatus(s)
        setError(false)
      })
      .catch(() => {
        setStatus('Unavailable')
        setError(true)
      })
  }, [])

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Index Status</h1>
      <div
        className={`p-4 rounded shadow text-lg ${
          error ? 'bg-error text-white' : 'bg-base-100'
        }`}
      >
        {status}
      </div>
    </div>
  )
}
