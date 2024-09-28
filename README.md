## Mô tả sơ lược:
Bên trên là back-end của một ứng dụng chatbot (Hỗ trợ người dùng về vẫn đề bệnh tim) bao gồm các chức năng chính như sau:
- Trả lời các câu hỏi FAQ
- Gợi ý thuốc theo tình hình bệnh và giá bệnh
- Dự đoán khả năng gặp bệnh tìm khi bạn cho biết các triệu chứng thường có

## Công nghệ sử dụng
- FastAPI: Là một framework web hiện đại dành cho Python, được tối ưu hóa về hiệu suất và dễ sử dụng. Nó giúp xây dựng các API RESTful nhanh chóng, hỗ trợ cả đồng bộ và bất đồng bộ (async).
- Alembic: Là một công cụ di trú (migration) cơ sở dữ liệu cho SQLAlchemy. Alembic giúp quản lý và theo dõi các thay đổi trong cấu trúc cơ sở dữ liệu (như thêm, sửa, xóa bảng hoặc cột) theo các phiên bản khác nhau.
- LangChain: Là một framework để xây dựng các ứng dụng AI bằng cách kết nối các mô hình ngôn ngữ (LLMs) và các công cụ khác. LangChain cung cấp cách dễ dàng để quản lý các mô hình, chuỗi hành động của AI, và tích hợp với các dịch vụ khác nhau.
- Together AI: Together AI là một nền tảng cung cấp các mô hình AI mở và phân tán. Nó có thể cung cấp các mô hình ngôn ngữ lớn (LLMs) thông qua một dịch vụ API để các nhà phát triển dễ dàng tích hợp vào ứng dụng của mình.
- PostgreSQL: PostgreSQL là một hệ quản trị cơ sở dữ liệu quan hệ mã nguồn mở mạnh mẽ, với khả năng xử lý dữ liệu lớn và hỗ trợ các tính năng nâng cao như khóa ngoại, triggers, và stored procedures.
- Poetry: Poetry là một công cụ quản lý gói và các dependencies cho các dự án Python. Nó giúp dễ dàng quản lý phiên bản của các thư viện, cài đặt các dependencies, và tạo ra các file pyproject.toml cho dự án.

## Mô hình hoạt động cơ bản

![image](https://github.com/user-attachments/assets/b63ce907-8a29-49e0-9c23-3224a95fe7a6)
