import { useState } from 'react'
import { uploadFile } from '../services/api'

export default function FileUpload() {
  const [file, setFile] = useState<File | null>(null)
  const [message, setMessage] = useState('')
  const [isError, setIsError] = useState(false)

  const handleUpload = async () => {
    if (!file) return
    setMessage('Uploading...')
    setIsError(false)
    try {
      await uploadFile(file)
      setMessage('✅ Upload successful!')
    } catch {
      setMessage('❌ Upload failed. Please try again.')
      setIsError(true)
    }
  }

  return (
    <div className="space-y-4">
      <input
        type="file"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
        className="file-input file-input-bordered w-full text-lg"
      />
      <button className="btn btn-primary btn-lg text-lg" onClick={handleUpload}>
        Upload
      </button>
      {message && (
        <div className={`text-md ${isError ? 'text-error' : 'text-success'}`}>
          {message}
        </div>
      )}
    </div>
  )
}
