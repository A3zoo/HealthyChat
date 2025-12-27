import { useState, useEffect, useRef } from 'react'
import MessageList from './MessageList'
import MessageInput from './MessageInput'
import { Message } from '../App'
import { Bot, Loader2 } from 'lucide-react'

interface ChatInterfaceProps {
  chatId: string
  userId: string
}

export default function ChatInterface({ chatId, userId }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [isInitialLoading, setIsInitialLoading] = useState(true)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    loadMessages()
  }, [chatId])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const loadMessages = async () => {
    try {
      setIsInitialLoading(true)
      const response = await fetch(
        `http://localhost:8000/api/messages/list/${chatId}?limit=50`,
        {
          headers: {
            'user_id': userId,
          },
        }
      )

      if (response.ok) {
        const data = await response.json()
        setMessages(data.messages || data || [])
      }
    } catch (error) {
      console.error('Error loading messages:', error)
    } finally {
      setIsInitialLoading(false)
    }
  }

  const handleSendMessage = async (content: string) => {
    if (!content.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      chat_id: chatId,
      user_id: userId,
      content: content.trim(),
      created_at: new Date().toISOString(),
    }

    // Optimistically add user message
    setMessages((prev) => [...prev, userMessage])
    setIsLoading(true)

    try {
      const response = await fetch('http://localhost:8000/api/message/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          chat_id: chatId,
          user_id: userId,
          content: content.trim(),
        }),
      })

      if (response.ok) {
        const botResponse = await response.json()
        
        // Add bot response
        const botMessage: Message = {
          id: (Date.now() + 1).toString(),
          chat_id: chatId,
          user_id: null,
          content: typeof botResponse === 'string' ? botResponse : botResponse.content || botResponse.message || '',
          created_at: new Date().toISOString(),
        }

        setMessages((prev) => [...prev, botMessage])
        
        // Reload messages to get the actual saved messages
        setTimeout(() => {
          loadMessages()
        }, 500)
      } else {
        throw new Error('Failed to send message')
      }
    } catch (error) {
      console.error('Error sending message:', error)
      // Remove optimistic message on error
      setMessages((prev) => prev.filter((msg) => msg.id !== userMessage.id))
      alert('Có lỗi xảy ra khi gửi tin nhắn. Vui lòng thử lại.')
    } finally {
      setIsLoading(false)
    }
  }

  if (isInitialLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-red-500 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Đang tải tin nhắn...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full bg-gradient-to-br from-red-50 via-white to-pink-50">
      {/* Welcome message if no messages */}
      {messages.length === 0 && (
        <div className="flex-1 flex items-center justify-center p-8">
          <div className="text-center max-w-2xl">
            <div className="bg-white rounded-full p-6 w-24 h-24 mx-auto mb-6 shadow-lg flex items-center justify-center">
              <Bot className="w-12 h-12 text-red-500" />
            </div>
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Chào mừng đến với HealthyChat! ❤️
            </h2>
            <p className="text-lg text-gray-600 mb-6">
              Tôi là chatbot tư vấn về sức khỏe tim mạch. Tôi có thể giúp bạn:
            </p>
            <div className="grid md:grid-cols-3 gap-4 text-left">
              <div className="bg-white p-4 rounded-lg shadow-md">
                <div className="text-2xl mb-2">💬</div>
                <h3 className="font-semibold mb-1">Trả lời FAQ</h3>
                <p className="text-sm text-gray-600">Câu hỏi thường gặp về bệnh tim</p>
              </div>
              <div className="bg-white p-4 rounded-lg shadow-md">
                <div className="text-2xl mb-2">💊</div>
                <h3 className="font-semibold mb-1">Gợi ý thuốc</h3>
                <p className="text-sm text-gray-600">Theo triệu chứng và ngân sách</p>
              </div>
              <div className="bg-white p-4 rounded-lg shadow-md">
                <div className="text-2xl mb-2">🔍</div>
                <h3 className="font-semibold mb-1">Dự đoán nguy cơ</h3>
                <p className="text-sm text-gray-600">Dựa trên triệu chứng của bạn</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Messages */}
      {messages.length > 0 && (
        <div className="flex-1 overflow-y-auto px-4 py-6">
          <MessageList messages={messages} />
          <div ref={messagesEndRef} />
        </div>
      )}

      {/* Input */}
      <div className="border-t border-gray-200 bg-white p-4">
        <MessageInput onSend={handleSendMessage} isLoading={isLoading} />
      </div>
    </div>
  )
}

