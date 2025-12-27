import { useState, useEffect, useRef } from 'react'
import ChatInterface from './components/ChatInterface'
import Header from './components/Header'
import { v4 as uuidv4 } from 'uuid'

export interface Message {
  id: string
  chat_id: string
  user_id: string | null
  content: string
  created_at: string
}

export interface Chat {
  id: string
  name: string
  user_id: string
  created_at: string
}

function App() {
  const [userId] = useState<string>(() => {
    // Lấy hoặc tạo user ID từ localStorage
    let id = localStorage.getItem('healthychat_user_id')
    if (!id) {
      id = uuidv4()
      localStorage.setItem('healthychat_user_id', id)
    }
    return id
  })

  const [currentChatId, setCurrentChatId] = useState<string | null>(null)

  useEffect(() => {
    // Tạo guest user nếu chưa có
    const createGuestUser = async () => {
      try {
        await fetch('http://localhost:8000/api/guest_user/create', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        })
      } catch (error) {
        console.error('Error creating guest user:', error)
      }
    }

    createGuestUser()
  }, [])

  const handleNewChat = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/chats', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: 'Cuộc trò chuyện mới',
          user_id: userId,
        }),
      })

      if (response.ok) {
        const chat = await response.json()
        setCurrentChatId(chat.id)
      }
    } catch (error) {
      console.error('Error creating chat:', error)
    }
  }

  useEffect(() => {
    // Tạo chat mới khi component mount
    if (!currentChatId) {
      handleNewChat()
    }
  }, [])

  return (
    <div className="flex flex-col h-screen">
      <Header onNewChat={handleNewChat} userId={userId} />
      <div className="flex-1 overflow-hidden">
        {currentChatId ? (
          <ChatInterface chatId={currentChatId} userId={userId} />
        ) : (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-500 mx-auto mb-4"></div>
              <p className="text-gray-600">Đang khởi tạo chat...</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App

