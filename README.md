# HealthyChat - Chatbot Tư Vấn Sức Khỏe Tim Mạch

## 📋 Mô Tả Dự Án

HealthyChat là một ứng dụng chatbot thông minh được xây dựng để hỗ trợ người dùng về các vấn đề liên quan đến bệnh tim mạch. Ứng dụng sử dụng công nghệ AI và vector embeddings để cung cấp các chức năng:

- **Trả lời các câu hỏi FAQ** về bệnh tim mạch
- **Gợi ý thuốc** theo tình trạng bệnh và ngân sách
- **Dự đoán nguy cơ bệnh tim** dựa trên các triệu chứng và tiền sử bệnh

## 🏗️ Kiến Trúc Hệ Thống

```
┌─────────────┐
│   Client    │
│  (Frontend) │
└──────┬──────┘
       │
       │ HTTP/REST API
       │
┌──────▼─────────────────────────────────────┐
│         FastAPI Backend                    │
│  ┌──────────────────────────────────────┐ │
│  │   Chat Service (LangChain Agent)     │ │
│  │  ┌──────────┐  ┌──────────┐         │ │
│  │  │  FAQ     │  │ Medicine │         │ │
│  │  │  Tool    │  │  Tool    │         │ │
│  │  └──────────┘  └──────────┘         │ │
│  │  ┌──────────┐                       │ │
│  │  │  Heart   │                       │ │
│  │  │ Prediction│                      │ │
│  │  └──────────┘                       │ │
│  └──────────────────────────────────────┘ │
│  ┌──────────────────────────────────────┐ │
│  │   Embedding Service                   │ │
│  │   (OpenAI text-embedding-3-small)     │ │
│  └──────────────────────────────────────┘ │
└──────┬─────────────────────────────────────┘
       │
       │ PostgreSQL + pgvector
       │
┌──────▼─────────────────────────────────────┐
│      PostgreSQL Database                   │
│  - Chat & Message Storage                  │
│  - Vector Store (FAQs, Medicine)           │
└────────────────────────────────────────────┘
```

## 🛠️ Công Nghệ Sử Dụng

### Backend Framework
- **FastAPI**: Framework web hiện đại, hiệu suất cao cho Python
- **Python 3.10+**: Ngôn ngữ lập trình chính

### AI & Machine Learning
- **LangChain**: Framework để xây dựng ứng dụng LLM
- **Together AI**: LLM provider (Mistralai/Mixtral-8x7B-Instruct-v0.1)
- **OpenAI Embeddings**: text-embedding-3-small cho vector embeddings
- **LangChain Agents**: Hệ thống agent với tool calling

### Database
- **PostgreSQL**: Database chính
- **pgvector**: Extension PostgreSQL cho vector similarity search
- **SQLAlchemy**: ORM cho Python
- **Alembic**: Database migration tool

### Development Tools
- **Poetry**: Dependency management
- **Pydantic**: Data validation
- **Black**: Code formatter

## 📦 Cài Đặt

### Yêu Cầu Hệ Thống
- Python 3.10 hoặc cao hơn
- PostgreSQL 12+ với extension pgvector
- Poetry (hoặc pip)

### Cài Đặt Dependencies

```bash
# Cài đặt Poetry (nếu chưa có)
curl -sSL https://install.python-poetry.org | python3 -

# Cài đặt dependencies
poetry install

# Hoặc sử dụng pip
pip install -r requirements.txt
```

### Cấu Hình Môi Trường

Tạo file `.env` trong thư mục gốc:

```env
# Together AI Configuration
TOGETHER_API_KEY=your_together_api_key_here

# Database Configuration
DB_NAME=healthychat
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Application Configuration
APP_ENV=development
DEBUG=true
```

### Khởi Tạo Database

```bash
# Tạo database
createdb healthychat

# Chạy migrations
alembic upgrade head

# Tạo extension pgvector (chạy trong PostgreSQL)
psql -d healthychat -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

### Chạy Ứng Dụng

```bash
# Development mode
poetry run uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Hoặc
python -m uvicorn app:app --reload
```

Ứng dụng sẽ chạy tại: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

## 🔍 Các Thành Phần Chính

### 1. Embedding Service

Hệ thống sử dụng **OpenAI text-embedding-3-small** để tạo vector embeddings cho:
- **FAQs**: Câu hỏi thường gặp về bệnh tim mạch
- **Medicine Database**: Thông tin về thuốc và điều trị

#### Cách Hoạt Động

```python
# Ví dụ từ tools/faq.py
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_postgres import PGVector

_vectors = PGVector(
    embeddings=OpenAIEmbeddings(model="text-embedding-3-small"),
    collection_name="faqs",
    connection=vectordb_conn_str,
    create_extension=True,
)
```

#### Thêm Dữ Liệu Vào Vector Store

```python
# Thêm FAQs
from langchain_core.documents import Document

documents = [
    Document(page_content="Câu hỏi: Bệnh tim có di truyền không?"),
    Document(page_content="Trả lời: Có, bệnh tim có thể di truyền...")
]

_vectors.add_documents(documents)
```

#### Vector Search

Hệ thống tự động sử dụng vector similarity search khi:
- Người dùng hỏi câu hỏi FAQ
- Tìm kiếm thuốc theo triệu chứng và giá

### 2. Chat Service

Chat service sử dụng **LangChain Agent** với các tools để xử lý cuộc trò chuyện.

#### Kiến Trúc Chat

```python
# Agent với 3 tools chính:
tools = [
    heart_predict_tool,  # Dự đoán bệnh tim
    faqs_tool,           # Trả lời FAQ
    medicine_tool        # Tìm thuốc
]

# Agent executor với conversation history
conversational_agent_executor = RunnableWithMessageHistory(
    agent_executor,
    get_history,  # Lấy lịch sử từ database
    input_messages_key="messages",
    output_messages_key="output",
)
```

#### API Endpoints

**Tạo Chat Mới:**
```bash
POST /api/chats
{
  "name": "Chat về bệnh tim",
  "user_id": "uuid-here"
}
```

**Gửi Tin Nhắn:**
```bash
POST /api/message/create
{
  "chat_id": "uuid-here",
  "user_id": "uuid-here",
  "content": "Tôi bị đau ngực, có phải bệnh tim không?"
}
```

**Lấy Lịch Sử Chat:**
```bash
GET /api/messages/list/{chat_id}?limit=20
Header: user_id: uuid-here
```

#### Conversation History

Hệ thống lưu trữ lịch sử chat trong PostgreSQL và sử dụng 10 tin nhắn gần nhất để duy trì ngữ cảnh cuộc trò chuyện.

### 3. Giao Diện (Interface)

#### Frontend Application

Dự án có một **React frontend** hiện đại với giao diện chat đẹp mắt và thân thiện với người dùng.

**Công nghệ Frontend:**
- React 18 + TypeScript
- Vite (build tool)
- TailwindCSS (styling)
- Lucide React (icons)
- React Markdown (render markdown)

**Cài đặt và Chạy Frontend:**

```bash
# Di chuyển vào thư mục frontend
cd frontend

# Cài đặt dependencies
npm install

# Chạy development server
npm run dev
```

Frontend sẽ chạy tại: `http://localhost:3000`

**Build Production:**

```bash
cd frontend
npm run build
```

**Cấu trúc Frontend:**

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.tsx          # Header với logo
│   │   ├── ChatInterface.tsx   # Component chính
│   │   ├── MessageList.tsx     # Danh sách messages
│   │   ├── MessageBubble.tsx   # Component message
│   │   └── MessageInput.tsx    # Input form
│   ├── App.tsx                 # Root component
│   └── main.tsx                # Entry point
```

**Tính năng Frontend:**
- ✅ Giao diện chat hiện đại, responsive
- ✅ Real-time messaging
- ✅ Markdown support cho bot responses
- ✅ Auto-scroll to latest message
- ✅ Loading states và error handling
- ✅ Local storage cho user session
- ✅ Smooth animations và transitions
- ✅ Welcome screen với thông tin về tính năng

#### API Documentation

FastAPI tự động tạo interactive API documentation:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

#### Frontend Integration

Backend hỗ trợ CORS để tích hợp với frontend:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cấu hình theo môi trường
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### Response Format

Tất cả API responses sử dụng JSON format:

```json
{
  "id": "uuid",
  "chat_id": "uuid",
  "user_id": "uuid",
  "content": "Nội dung tin nhắn",
  "created_at": "2024-01-01T00:00:00Z"
}
```

## 🐳 Docker

### Dockerfile

Dự án đã được containerized với Docker để dễ dàng triển khai.

#### Build Docker Image

```bash
docker build -t healthychat:latest .
```

#### Chạy Container

```bash
docker run -d \
  --name healthychat \
  -p 8000:8000 \
  --env-file .env \
  healthychat:latest
```

#### Docker Compose

Sử dụng `docker-compose.yml` để chạy toàn bộ stack (app + database):

```bash
# Khởi động tất cả services
docker-compose up -d

# Xem logs
docker-compose logs -f

# Dừng services
docker-compose down
```

#### Environment Variables trong Docker

Đảm bảo file `.env` có đầy đủ các biến môi trường cần thiết hoặc truyền trực tiếp:

```bash
docker run -d \
  -e TOGETHER_API_KEY=your_key \
  -e DB_HOST=postgres \
  -e DB_NAME=healthychat \
  -e DB_USER=postgres \
  -e DB_PASSWORD=password \
  healthychat:latest
```

## 🎯 Event-Driven Architecture (EDA)

Dự án sử dụng **Event-Driven Architecture** để tách biệt các components và cho phép hệ thống phản ứng với các sự kiện một cách linh hoạt.

### Kiến Trúc Event-Driven

```
┌─────────────────────────────────────────┐
│         Event Publishers                │
│  (Repository Layer)                     │
│  - create_message()                     │
│  - create_chat()                        │
└──────────────┬──────────────────────────┘
               │
               │ Publish Events
               │
┌──────────────▼──────────────────────────┐
│           Event Bus                     │
│  - subscribe()                          │
│  - publish()                            │
│  - get_event_history()                  │
└──────────────┬──────────────────────────┘
               │
               │ Dispatch to Handlers
               │
┌──────────────▼──────────────────────────┐
│         Event Handlers                  │
│  - message_created_handler()            │
│  - chat_created_handler()               │
│  - heart_prediction_handler()           │
└──────────────┬──────────────────────────┘
               │
               │ Update State / Notifications
               │
┌──────────────▼──────────────────────────┐
│      Notification Store                  │
│  (In-memory, có thể thay bằng Redis)     │
└──────────────────────────────────────────┘
```

### Các Thành Phần Chính

#### 1. Event Bus (`events/event_bus.py`)

Event Bus là trung tâm của hệ thống event-driven, quản lý việc publish và subscribe events.

**Tính năng:**
- **Publish/Subscribe Pattern**: Components có thể publish events và subscribe để nhận events
- **Event History**: Lưu trữ lịch sử events (tối đa 100 events)
- **Error Handling**: Tự động xử lý lỗi trong handlers, không làm gián đoạn hệ thống
- **Wildcard Subscriptions**: Hỗ trợ subscribe tất cả events với `"*"`

**Ví dụ sử dụng:**
```python
from events.event_bus import event_bus
from events.event_models import MessageCreatedEvent

# Publish event
event = MessageCreatedEvent(
    chat_id=chat_id,
    user_id=user_id,
    message_id=message_id,
    content="Hello",
    is_bot_message=False
)
event_bus.publish(event)

# Subscribe handler
def my_handler(event: BaseEvent):
    print(f"Received event: {event.event_type}")

event_bus.subscribe("message.created", my_handler)
```

#### 2. Event Types (`events/event_types.py`)

Định nghĩa các loại events trong hệ thống:

- `MESSAGE_CREATED`: Khi có tin nhắn mới được tạo
- `CHAT_CREATED`: Khi có chat mới được tạo
- `HEART_PREDICTION_COMPLETED`: Khi hoàn thành dự đoán bệnh tim
- `MEDICINE_RECOMMENDED`: Khi có gợi ý thuốc
- `FAQ_ANSWERED`: Khi trả lời câu hỏi FAQ

#### 3. Event Models (`events/event_models.py`)

Các event models kế thừa từ `BaseEvent`:

- **BaseEvent**: Base class với `event_type`, `timestamp`, `event_id`, `metadata`
- **MessageCreatedEvent**: Event khi tạo message
- **ChatCreatedEvent**: Event khi tạo chat
- **HeartPredictionCompletedEvent**: Event khi hoàn thành dự đoán
- **MedicineRecommendedEvent**: Event khi có gợi ý thuốc

#### 4. Event Handlers (`events/event_handlers.py`)

Các handlers xử lý events:

**message_created_handler:**
- Tạo notification khi bot trả lời
- Lưu vào notification store
- Có thể tích hợp với email/SMS service

**chat_created_handler:**
- Log analytics
- Tạo welcome notification
- Có thể trigger onboarding flow

**heart_prediction_handler:**
- Tạo notification với risk level
- Có thể trigger follow-up actions
- Lưu kết quả vào analytics

#### 5. Integration với Repository Layer

Events được publish tự động trong repository methods:

```python
# repository/message.py
def create_message(payload: CreateMessageModel):
    # ... tạo message trong database ...
    
    # Publish event - Event-Driven Architecture
    event = MessageCreatedEvent(...)
    event_bus.publish(event)
    
    return message_model
```

### Demo: Real-time Notifications

Hệ thống có một **Notification Center** trong frontend để demo Event-Driven Architecture:

**Tính năng:**
- ✅ Real-time notifications khi bot trả lời
- ✅ Notifications khi tạo chat mới
- ✅ Notifications khi có kết quả dự đoán bệnh tim
- ✅ Auto-refresh mỗi 3 giây
- ✅ Unread count badge

**API Endpoints:**

```bash
# Lấy notifications
GET /api/notifications
Header: user_id: uuid-here

# Xóa notifications
DELETE /api/notifications
Header: user_id: uuid-here

# Lấy số lượng unread
GET /api/notifications/unread-count
Header: user_id: uuid-here
```

**Frontend Component:**

Notification Center được tích hợp vào Header component, tự động poll notifications và hiển thị badge với số lượng unread.

### Lợi Ích của Event-Driven Architecture

1. **Decoupling**: Components không cần biết về nhau, chỉ cần biết về events
2. **Scalability**: Dễ dàng thêm handlers mới mà không ảnh hưởng code hiện tại
3. **Flexibility**: Có thể thay đổi behavior bằng cách thêm/bớt handlers
4. **Testability**: Dễ test từng handler riêng biệt
5. **Extensibility**: Dễ dàng mở rộng với background jobs, webhooks, etc.

### Mở Rộng trong Tương Lai

- **Redis Pub/Sub**: Thay thế in-memory store bằng Redis cho distributed systems
- **Message Queue**: Tích hợp RabbitMQ/Kafka cho async processing
- **Webhooks**: Gửi events đến external services
- **Event Sourcing**: Lưu tất cả events để replay state
- **CQRS**: Tách read/write models với events

## 🔄 CI/CD

Dự án sử dụng **GitHub Actions** để tự động hóa quy trình CI/CD.

### Workflow Files

#### 1. CI Pipeline (`.github/workflows/ci.yml`)

Tự động chạy khi có push hoặc pull request:
- Lint code với Black
- Chạy tests
- Kiểm tra code quality

#### 2. CD Pipeline (`.github/workflows/cd.yml`)

Tự động deploy khi merge vào main branch:
- Build Docker image
- Push image lên Docker Hub / Container Registry
- Deploy lên production server

### Cấu Hình CI/CD

#### Secrets cần thiết trong GitHub:

Thêm các secrets sau vào GitHub repository (Settings → Secrets and variables → Actions):

- `TOGETHER_API_KEY`: API key cho Together AI
- `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`: Database credentials
- `DOCKER_USERNAME`, `DOCKER_PASSWORD`: Docker Hub credentials (nếu sử dụng)
- `DEPLOY_HOST`: Địa chỉ IP hoặc domain của production server (ví dụ: `192.168.1.100` hoặc `deploy.example.com`)
- `DEPLOY_USER`: Username SSH để đăng nhập vào server (ví dụ: `ubuntu` hoặc `deploy`)
- `DEPLOY_SSH_KEY`: Private SSH key để kết nối với server

#### Setup Production Server

Trên server production, cần chuẩn bị:

1. **Tạo thư mục deployment:**
```bash
# SSH vào server
ssh user@your-server

# Tạo thư mục (mặc định là /opt/healthychat)
sudo mkdir -p /opt/healthychat
sudo chown $USER:$USER /opt/healthychat
cd /opt/healthychat
```

2. **Tạo file docker-compose.yml và .env:**
```bash
# Copy docker-compose.yml từ repo
# Tạo file .env với các biến môi trường cần thiết
nano .env
```

3. **Cấu hình SSH key:**
```bash
# Tạo SSH key pair nếu chưa có
ssh-keygen -t rsa -b 4096 -C "github-actions"

# Copy public key vào server
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

# Copy private key vào GitHub Secrets (DEPLOY_SSH_KEY)
cat ~/.ssh/id_rsa
```

**Lưu ý:** Đường dẫn deployment mặc định là `/opt/healthychat`. Nếu muốn thay đổi, sửa trong file `.github/workflows/cd.yml` dòng 45:
```yaml
cd /opt/healthychat  # Thay đổi đường dẫn tại đây
```

#### Manual Trigger

Workflow cũng có thể được trigger thủ công từ GitHub Actions tab:
1. Vào tab "Actions" trên GitHub
2. Chọn workflow "CD"
3. Click "Run workflow"
4. Chọn branch và click "Run workflow"

### Deployment Strategy

1. **Development**: Tự động deploy sau mỗi commit vào `develop` branch
2. **Staging**: Tự động deploy sau merge vào `staging` branch  
3. **Production**: Tự động deploy sau merge vào `main` branch (có thể yêu cầu approval)

### Quy Trình Deployment

Khi code được push lên `main` branch, CD pipeline sẽ:

1. **Build Docker Image**: Build image từ Dockerfile
2. **Push to Registry**: Push image lên Docker Hub với tags:
   - `username/healthychat:latest`
   - `username/healthychat:commit-sha`
3. **Deploy to Server**: 
   - SSH vào production server
   - `cd /opt/healthychat` (hoặc thư mục bạn đã cấu hình)
   - Pull Docker image mới nhất
   - Restart containers với `docker-compose up -d`
   - Chạy database migrations
   - Clean up unused Docker resources

## 📁 Cấu Trúc Thư Mục

```
HealthyChat/
├── alembic/              # Database migrations
├── controllers/          # API route handlers
│   ├── chat.py
│   ├── chat_message.py
│   ├── user.py
│   └── notifications.py  # Notifications API (Event-Driven)
├── events/                # Event-Driven Architecture
│   ├── __init__.py
│   ├── event_bus.py       # Event Bus implementation
│   ├── event_types.py     # Event type definitions
│   ├── event_models.py    # Event models (Pydantic)
│   └── event_handlers.py  # Event handlers
├── models/               # SQLAlchemy models & Pydantic schemas
│   ├── chat.py
│   ├── message.py
│   └── user.py
├── repository/           # Data access layer
│   ├── chat.py           # Publishes ChatCreatedEvent
│   └── message.py        # Publishes MessageCreatedEvent
├── services/             # Business logic
│   ├── chat_with_AI.py   # Main chat service
│   └── together_AI.py    # LLM configuration
├── tools/                # LangChain tools
│   ├── faq.py           # FAQ retrieval tool
│   ├── heart_prediction.py  # Heart disease prediction
│   └── medicine.py      # Medicine recommendation
├── frontend/             # React frontend application
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.tsx
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── MessageList.tsx
│   │   │   ├── MessageBubble.tsx
│   │   │   ├── MessageInput.tsx
│   │   │   └── NotificationCenter.tsx  # Event-Driven Demo
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── app.py               # FastAPI application entry point
├── app_env.py           # Environment configuration
├── database.py          # Database connection
├── pyproject.toml       # Poetry dependencies
├── alembic.ini          # Alembic configuration
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose configuration
└── README.md            # This file
```

## 🧪 Testing

```bash
# Chạy tests
poetry run pytest

# Với coverage
poetry run pytest --cov=. --cov-report=html
```

## 📝 API Examples

### Tạo Chat và Gửi Tin Nhắn

```bash
# 1. Tạo chat mới
curl -X POST "http://localhost:8000/api/chats" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tư vấn bệnh tim",
    "user_id": "123e4567-e89b-12d3-a456-426614174000"
  }'

# 2. Gửi tin nhắn
curl -X POST "http://localhost:8000/api/message/create" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "chat-uuid-here",
    "user_id": "user-uuid-here",
    "content": "Tôi bị đau ngực khi vận động, có phải bệnh tim không?"
  }'

# 3. Lấy lịch sử chat
curl -X GET "http://localhost:8000/api/messages/list/chat-uuid-here?limit=20" \
  -H "user_id: user-uuid-here"
```

## 🔒 Security

- Sử dụng environment variables cho sensitive data
- CORS được cấu hình phù hợp với môi trường
- Database credentials không được hardcode
- API keys được quản lý qua environment variables

## 📚 Tài Liệu Tham Khảo

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [PostgreSQL pgvector](https://github.com/pgvector/pgvector)
- [Together AI](https://together.ai/)

## 🤝 Đóng Góp

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

- **TripHunter** - *Initial work* - [TripHunter](https://triphunter.vn)

## 🙏 Acknowledgments

- OpenAI cho embedding model
- Together AI cho LLM service
- LangChain team cho framework tuyệt vời
