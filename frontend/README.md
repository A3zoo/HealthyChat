# HealthyChat Frontend

Frontend cho ứng dụng HealthyChat - Chatbot Tư Vấn Sức Khỏe Tim Mạch.

## 🚀 Công Nghệ

- **React 18** - UI Framework
- **TypeScript** - Type safety
- **Vite** - Build tool nhanh
- **TailwindCSS** - Styling
- **Lucide React** - Icons
- **React Markdown** - Render markdown messages

## 📦 Cài Đặt

```bash
# Cài đặt dependencies
npm install

# Hoặc sử dụng yarn
yarn install

# Hoặc pnpm
pnpm install
```

## 🏃 Chạy Development Server

```bash
npm run dev
```

Ứng dụng sẽ chạy tại: `http://localhost:3000`

## 🏗️ Build Production

```bash
npm run build
```

Files sẽ được build vào thư mục `dist/`

## 📁 Cấu Trúc Thư Mục

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.tsx          # Header với logo và nút tạo chat mới
│   │   ├── ChatInterface.tsx   # Component chính cho chat interface
│   │   ├── MessageList.tsx     # Danh sách messages
│   │   ├── MessageBubble.tsx   # Component cho từng message
│   │   └── MessageInput.tsx    # Input để gửi message
│   ├── App.tsx                 # Root component
│   ├── main.tsx                # Entry point
│   └── index.css               # Global styles
├── index.html
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── vite.config.ts
```

## 🔌 API Integration

Frontend tích hợp với backend API tại `http://localhost:8000`:

- `POST /api/guest_user/create` - Tạo guest user
- `POST /api/chats` - Tạo chat mới
- `POST /api/message/create` - Gửi message
- `GET /api/messages/list/{chat_id}` - Lấy danh sách messages

## 🎨 Features

- ✅ Modern, responsive UI
- ✅ Real-time chat interface
- ✅ Markdown support cho bot messages
- ✅ Auto-scroll to latest message
- ✅ Loading states
- ✅ Error handling
- ✅ Local storage cho user ID
- ✅ Smooth animations

## 🌐 Environment Variables

Có thể tạo file `.env` để cấu hình:

```env
VITE_API_URL=http://localhost:8000
```

