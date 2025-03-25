import { useEffect, useState } from 'react'
import FileUpload from '../components/FileUpload'
import { listFiles } from '../services/api'
import type { FileInfo } from '../types/FileInfo'
import { formatDate } from '../utils/formatDate'

export default function UploadPage() {
  const [files, setFiles] = useState<FileInfo[]>([])

  useEffect(() => {
    listFiles()
      .then(setFiles)
      .catch(() => setFiles([]))
  }, [])

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold">Upload PDF</h1>
      <FileUpload />
      <h2 className="text-xl font-semibold">Uploaded Files</h2>
      <div className="overflow-x-auto text-lg">
        <table className="table table-zebra w-full">
          <thead>
            <tr>
              <th>Filename</th>
              <th>Size</th>
              <th>Uploaded</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {files.map((file) => (
              <tr key={file.filename}>
                <td>{file.filename}</td>
                <td>{(file.size / 1024).toFixed(2)} KB</td>
                <td>{formatDate(file.uploadedAt)}</td>
                <td>
                  {file.indexed ? (
                    <span className="badge badge-success badge-lg">
                      Indexed
                    </span>
                  ) : (
                    <span className="badge badge-warning badge-lg">
                      Pending
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
