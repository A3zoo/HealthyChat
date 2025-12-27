import { useState, useEffect } from 'react'
import { Bell, X, Heart, MessageSquare, AlertCircle } from 'lucide-react'

interface Notification {
  type: string
  chat_id?: string
  message_id?: string
  content?: string
  message?: string
  risk_level?: string
  timestamp: string
}

interface NotificationCenterProps {
  userId: string
}

export default function NotificationCenter({ userId }: NotificationCenterProps) {
  const [notifications, setNotifications] = useState<Notification[]>([])
  const [isOpen, setIsOpen] = useState(false)
  const [unreadCount, setUnreadCount] = useState(0)

  const fetchNotifications = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/notifications?limit=10`,
        {
          headers: {
            'user_id': userId,
          },
        }
      )

      if (response.ok) {
        const data = await response.json()
        setNotifications(data.notifications || [])
        setUnreadCount(data.total || 0)
      }
    } catch (error) {
      console.error('Error fetching notifications:', error)
    }
  }

  useEffect(() => {
    fetchNotifications()
    // Poll for new notifications every 3 seconds (Event-Driven Architecture Demo)
    const interval = setInterval(fetchNotifications, 3000)
    return () => clearInterval(interval)
  }, [userId])

  const clearNotifications = async () => {
    try {
      await fetch('http://localhost:8000/api/notifications', {
        method: 'DELETE',
        headers: {
          'user_id': userId,
        },
      })
      setNotifications([])
      setUnreadCount(0)
    } catch (error) {
      console.error('Error clearing notifications:', error)
    }
  }

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'heart_prediction':
        return <Heart className="w-5 h-5 text-red-500" />
      case 'message':
        return <MessageSquare className="w-5 h-5 text-blue-500" />
      default:
        return <AlertCircle className="w-5 h-5 text-gray-500" />
    }
  }

  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diff = now.getTime() - date.getTime()
    const seconds = Math.floor(diff / 1000)
    const minutes = Math.floor(seconds / 60)

    if (minutes < 1) return 'Vừa xong'
    if (minutes < 60) return `${minutes} phút trước`
    return date.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
  }

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="relative p-2 text-gray-600 hover:text-red-500 transition-colors"
      >
        <Bell className="w-6 h-6" />
        {unreadCount > 0 && (
          <span className="absolute top-0 right-0 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
            {unreadCount > 9 ? '9+' : unreadCount}
          </span>
        )}
      </button>

      {isOpen && (
        <>
          <div
            className="fixed inset-0 z-40"
            onClick={() => setIsOpen(false)}
          />
          <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-xl z-50 border border-gray-200">
            <div className="p-4 border-b border-gray-200 flex items-center justify-between">
              <h3 className="font-semibold text-gray-900">Thông báo</h3>
              <div className="flex items-center space-x-2">
                {unreadCount > 0 && (
                  <button
                    onClick={clearNotifications}
                    className="text-xs text-gray-500 hover:text-red-500"
                  >
                    Xóa tất cả
                  </button>
                )}
                <button
                  onClick={() => setIsOpen(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>

            <div className="max-h-96 overflow-y-auto">
              {notifications.length === 0 ? (
                <div className="p-8 text-center text-gray-500">
                  <Bell className="w-12 h-12 mx-auto mb-2 opacity-50" />
                  <p>Chưa có thông báo</p>
                </div>
              ) : (
                <div className="divide-y divide-gray-100">
                  {notifications
                    .slice()
                    .reverse()
                    .map((notification, index) => (
                      <div
                        key={index}
                        className="p-4 hover:bg-gray-50 transition-colors animate-fade-in"
                      >
                        <div className="flex items-start space-x-3">
                          <div className="flex-shrink-0 mt-1">
                            {getNotificationIcon(notification.type)}
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className="text-sm text-gray-900">
                              {notification.message ||
                                notification.content ||
                                'Thông báo mới'}
                            </p>
                            {notification.risk_level && (
                              <span
                                className={`inline-block mt-1 px-2 py-1 text-xs rounded-full ${
                                  notification.risk_level === 'high'
                                    ? 'bg-red-100 text-red-800'
                                    : notification.risk_level === 'medium'
                                    ? 'bg-yellow-100 text-yellow-800'
                                    : 'bg-green-100 text-green-800'
                                }`}
                              >
                                {notification.risk_level === 'high'
                                  ? 'Nguy cơ cao'
                                  : notification.risk_level === 'medium'
                                  ? 'Nguy cơ trung bình'
                                  : 'Nguy cơ thấp'}
                              </span>
                            )}
                            <p className="text-xs text-gray-500 mt-1">
                              {formatTime(notification.timestamp)}
                            </p>
                          </div>
                        </div>
                      </div>
                    ))}
                </div>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  )
}

