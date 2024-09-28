from langchain_postgres import PGVector
from langchain_openai.embeddings import OpenAIEmbeddings
from database import vectordb_conn_str
from langchain_core.tools import create_retriever_tool


# FAQs retrieval tool
_vectors = PGVector(
    embeddings=OpenAIEmbeddings(model="text-embedding-3-small"),
    collection_name="faqs",
    connection=vectordb_conn_str,
    create_extension=True,
)
faqs_retriever = _vectors.as_retriever()

faqs_tool = create_retriever_tool(
    faqs_retriever,
    "faqs_retriever",
    "Tìm kiếm và trả về câu trả lời cho câu hỏi thường gặp của khách hàng về TripHunter và dichj vụ của TripHunter",
)