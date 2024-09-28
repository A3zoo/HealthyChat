from uuid import UUID
from database import db
from langchain_postgres import PGVector
from langchain_core.tools import StructuredTool
from langchain_openai.embeddings import OpenAIEmbeddings
from pydantic import BaseModel, Field
from typing import Optional

# Create hotel vector
_vectors = PGVector(
    embeddings=OpenAIEmbeddings(model="text-embedding-3-small"),
    collection_name="medicine",
    connection=db,
    create_extension=True,
)

medicine_retriever = _vectors.as_retriever()

class InputInfor(BaseModel):
    """
    Thông tin được lấy từ lịch sử chat giữa bạn và khách hàng
    Field:
        price: Giá của thuốc
        symptom: Chịu chứng mắc phải của người bệnh
    """

    price: Optional[str] = Field(
        description=" Giá của thuốc"
    )

    symptom: Optional[str] = Field(description="Chịu chứng mắc phải của người bệnh")


def find_medicine(
    price: Optional[str] = None,
    symptom: Optional[str] = None,
):
    """Đề xuất khách sạn phù hợp với các yêu cầu của khách hàng.
    Args:
        price: Giá của thuốc
        symptom: Chịu chứng mắc phải của người bệnh
    Returns:
        List danh sách các loại thuốc
    """
    if price == None:
        return "chatbot hãy hỏi lại khách hàng về giá của thuốc"
    if symptom == None:
        return "chabot hãy hỏi lại khách hàng triệu chứng của mình"
    return medicine_retriever.invoke(
        f"Giá: {price} \n\
        Triệu chứng: {symptom}   
        "
    )


medicine_tool = StructuredTool.from_function(
    find_medicine,
    name="find_medicine_tool",
    args_schema=InputInfor,
    description=(
        "Đây là công cụ tra cứu thuốc theo giá và triệu chứng bệnh"
    ),
)
