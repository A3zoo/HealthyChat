import { useState, KeyboardEvent } from 'react'
import { Send, Loader2 } from 'lucide-react'

interface MessageInputProps {
  onSend: (message: string) => void
  isLoading: boolean
}

export default function MessageInput({ onSend, isLoading }: MessageInputProps) {
  const [message, setMessage] = useState('')

  const handleSend = () => {
    if (message.trim() && !isLoading) {
      onSend(message)
      setMessage('')
    }
  }

  const handleKeyPress = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex items-end space-x-3 bg-white rounded-full px-4 py-2 shadow-lg border border-gray-200">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Nhập câu hỏi của bạn về bệnh tim mạch..."
          className="flex-1 resize-none border-none outline-none px-4 py-2 max-h-32 overflow-y-auto bg-transparent text-gray-800 placeholder-gray-400"
          rows={1}
          disabled={isLoading}
        />
        <button
          onClick={handleSend}
          disabled={!message.trim() || isLoading}
          className="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-r from-red-500 to-pink-500 text-white flex items-center justify-center hover:from-red-600 hover:to-pink-600 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-md hover:shadow-lg"
        >
          {isLoading ? (
            <Loader2 className="w-5 h-5 animate-spin" />
          ) : (
            <Send className="w-5 h-5" />
          )}
        </button>
      </div>
      <p className="text-xs text-gray-500 mt-2 text-center">
        Nhấn Enter để gửi, Shift + Enter để xuống dòng
      </p>
    </div>
  )
}

