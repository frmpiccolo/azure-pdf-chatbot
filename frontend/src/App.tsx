import { BrowserRouter, Routes, Route } from 'react-router-dom'
import ChatPage from './pages/ChatPage'
import UploadPage from './pages/UploadPage'
import IndexStatusPage from './pages/IndexStatusPage'
import Layout from './layouts/Layout'

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<UploadPage />} />
          <Route path="/status" element={<IndexStatusPage />} />
          <Route path="/chat" element={<ChatPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}
