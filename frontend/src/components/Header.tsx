import React from 'react'
import { Link } from 'react-router-dom'
import logo from '../assets/logo.png'

export default function Header() {
  return (
    <header className="bg-base-100 rounded-2xl shadow px-6 py-4 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <img src={logo} alt="Logo" className="w-20 h-20" />
        <Link to="/" className="text-2xl font-bold text-primary">
          PDF Chatbot
        </Link>
      </div>
      <nav className="flex gap-2">
        <Link to="/" className="btn btn-ghost text-lg">
          Upload
        </Link>
        <Link to="/status" className="btn btn-ghost text-lg">
          Status
        </Link>
        <Link to="/chat" className="btn btn-ghost text-lg">
          Chat
        </Link>
      </nav>
    </header>
  )
}
