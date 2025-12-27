import { Message } from '../App'
import { User, Bot } from 'lucide-react'
import ReactMarkdown from 'react-markdown'

interface MessageBubbleProps {
  message: Message
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.user_id !== null

  return (
    <div
      className={`flex items-start space-x-3 animate-fade-in ${
        isUser ? 'flex-row-reverse space-x-reverse' : ''
      }`}
    >
      {/* Avatar */}
      <div
        className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
          isUser
            ? 'bg-gradient-to-br from-red-500 to-pink-500'
            : 'bg-gradient-to-br from-gray-100 to-gray-200'
        }`}
      >
        {isUser ? (
          <User className="w-5 h-5 text-white" />
        ) : (
          <Bot className="w-5 h-5 text-gray-700" />
        )}
      </div>

      {/* Message */}
      <div
        className={`flex flex-col ${
          isUser ? 'items-end' : 'items-start'
        } max-w-[75%]`}
      >
        <div
          className={`message-bubble ${
            isUser ? 'message-user' : 'message-bot'
          } animate-slide-up`}
        >
          <div className={isUser ? 'text-white' : 'text-gray-800'}>
            <ReactMarkdown
              className="prose prose-sm max-w-none"
              components={{
                p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
                ul: ({ children }) => (
                  <ul className="list-disc list-inside mb-2 space-y-1">{children}</ul>
                ),
                ol: ({ children }) => (
                  <ol className="list-decimal list-inside mb-2 space-y-1">{children}</ol>
                ),
                strong: ({ children }) => (
                  <strong className="font-semibold">{children}</strong>
                ),
                em: ({ children }) => <em className="italic">{children}</em>,
              }}
            >
              {message.content}
            </ReactMarkdown>
          </div>
        </div>
        <span className="text-xs text-gray-500 mt-1 px-2">
          {new Date(message.created_at).toLocaleTimeString('vi-VN', {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </span>
      </div>
    </div>
  )
}

