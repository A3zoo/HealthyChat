import { Heart, MessageSquarePlus } from 'lucide-react'
import NotificationCenter from './NotificationCenter'

interface HeaderProps {
  onNewChat: () => void
  userId: string
}

export default function Header({ onNewChat, userId }: HeaderProps) {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-3">
            <div className="bg-gradient-to-br from-red-500 to-pink-500 p-2 rounded-lg">
              <Heart className="w-6 h-6 text-white" fill="currentColor" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">HealthyChat</h1>
              <p className="text-xs text-gray-500">Tư vấn sức khỏe tim mạch</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            {/* Event-Driven Architecture Demo: Notification Center */}
            <NotificationCenter userId={userId} />
            
            <button
              onClick={onNewChat}
              className="flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-red-500 to-pink-500 text-white rounded-lg hover:from-red-600 hover:to-pink-600 transition-all duration-200 shadow-md hover:shadow-lg"
            >
              <MessageSquarePlus className="w-5 h-5" />
              <span className="hidden sm:inline">Cuộc trò chuyện mới</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}

