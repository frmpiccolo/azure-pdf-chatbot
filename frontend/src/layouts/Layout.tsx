import React, { ReactNode } from 'react'
import Header from '../components/Header'

interface Props {
  children: ReactNode
}

export default function Layout({ children }: Props) {
  return (
    <div className="min-h-screen bg-base-200 text-base-content px-4 py-10">
      <div className="max-w-4xl mx-auto space-y-8">
        <Header />
        <main className="bg-base-100 p-10 rounded-2xl shadow-lg min-h-[600px]">
          {children}
        </main>
      </div>
    </div>
  )
}
