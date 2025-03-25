import { useState } from 'react'
import { askQuestion } from '../services/api'
import type { ChatMessage } from '../types/ChatMessage'

export default function ChatBox() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [error, setError] = useState<string>('')

  const send = async () => {
    if (!input.trim()) return

    setError('')
    const userMessage: ChatMessage = { role: 'user', content: input }
    setMessages((prev) => [...prev, userMessage])
    setInput('')

    try {
      const answer = await askQuestion(input)
      const botMessage: ChatMessage = { role: 'bot', content: answer }
      setMessages((prev) => [...prev, botMessage])
    } catch {
      const botMessage: ChatMessage = {
        role: 'bot',
        content: 'Sorry, I could not get a response. Please try again later.',
      }
      setMessages((prev) => [...prev, botMessage])
      setError('Something went wrong while processing your question.')
    }
  }

  return (
    <div className="space-y-4">
      <div className="bg-base-100 p-4 rounded shadow max-h-[400px] overflow-y-auto text-lg">
        {messages.map((m, i) => (
          <div
            key={i}
            className={`mb-2 ${m.role === 'user' ? 'text-right' : 'text-left'}`}
          >
            <div
              className={`inline-block px-4 py-2 rounded-lg max-w-xs break-words ${
                m.role === 'user'
                  ? 'bg-primary text-white'
                  : 'bg-base-200 text-base-content'
              }`}
            >
              {m.content}
            </div>
          </div>
        ))}
      </div>
      <div className="flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="input input-bordered w-full text-lg"
          placeholder="Ask something..."
        />
        <button className="btn btn-secondary btn-lg text-lg" onClick={send}>
          Send
        </button>
      </div>
      {error && <div className="text-error text-sm">{error}</div>}
    </div>
  )
}
