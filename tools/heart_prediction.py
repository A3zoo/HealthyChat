from uuid import UUID
from database import db
from langchain_postgres import PGVector
from langchain_core.tools import StructuredTool
from langchain_openai.embeddings import OpenAIEmbeddings
from pydantic import BaseModel, Field
from typing import Optional

class InputInfor(BaseModel):
    """
    Đưới đây là các triệu chứng mà có nguy cơ xảy ra bệnh tim cao nhất theo khảo sát
    Field:
        HadAngina: đau thắc ngực
        HadAsthma: Bị hen xuyễn
        HadCOPD: Người tham gia có từng bị bệnh phổi tắc nghẽn mạn tính (COPD) không.
        HadDepressiveDisorder: Người tham gia có từng bị rối loạn trầm cảm không.
        HadKidneyDisease: Người tham gia có từng bị bệnh thận không.
        HadArthritis: Người tham gia có từng bị viêm khớp không.
        HadDiabetes: Người tham gia có từng bị bệnh tiểu đường không.
        DeafOrHardOfHearing: Người tham gia có bị điếc hoặc khó nghe không.
        BlindOrVisionDifficulty: Người tham gia có bị mù hoặc gặp khó khăn về thị lực không.
    """

    HadAngina: Optional[bool] = Field(
        description="Đau thắc ngực"
    )
    HadAsthma: Optional[bool] = Field(
        description="Bị hen xuyễn"
    )
    HadCOPD: Optional[bool] = Field(
        description=" Người tham gia có từng bị bệnh phổi tắc nghẽn mạn tính (COPD) không."
    )
    HadDepressiveDisorder: Optional[bool] = Field(
        description="Người tham gia có từng bị rối loạn trầm cảm không."
    )
    HadKidneyDisease: Optional[bool] = Field(
        description="Người tham gia có từng bị bệnh thận không."
    )
    HadArthritis: Optional[bool] = Field(
        description=" Người tham gia có từng bị viêm khớp không."
    )
    HadDiabetes: Optional[bool] = Field(
        description="Người tham gia có từng bị bệnh tiểu đường không."
    )
    HadADeafOrHardOfHearingngina: Optional[bool] = Field(
        description="Người tham gia có bị điếc hoặc khó nghe không."
    )
    BlindOrVisionDifficulty: Optional[bool] = Field(
        description="Người tham gia có bị mù hoặc gặp khó khăn về thị lực không."
    )


def predict(
    HadAngina: Optional[str] = None,
    HadAsthma: Optional[str] = None,
    HadCOPD: Optional[str] = None,
    HadDepressiveDisorder: Optional[str] = None,
    HadKidneyDisease: Optional[str] = None,
    HadArthritis: Optional[str] = None,
    HadDiabetes: Optional[str] = None,
    DeafOrHardOfHearing: Optional[str] = None,
    BlindOrVisionDifficulty: Optional[str] = None,
):
    
    # Trả về kết quả dự đoán theo mô hình
    return 
    


heart_predict_tool = StructuredTool.from_function(
    predict,
    name="heart_predict_tool",
    args_schema=InputInfor,
    description=(
        "Đây là công cụ chuẩn đoán xem khách hàng có bị mắc bệnh tim hay không. "
        "Và trước khi thực hiện chuẩn đoán hãy hỏi khách hàng các thông tin trong args_schema"
    ),
)
