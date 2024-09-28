from uuid import UUID
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.chat_history import BaseChatMessageHistory
from langchain.agents import AgentExecutor, create_tool_calling_agent
from together_AI import llm
from repository.message import get_messages, create_message
from langchain_community.chat_message_histories import ChatMessageHistory
from tools.medicine import heart_predict_tool
from tools.faq import faqs_tool
from tools.medicine import medicine_tool
from models.message import CreateMessageModel


def get_history(session_id: UUID) -> BaseChatMessageHistory:
    history = ChatMessageHistory()
    db_messages = get_messages(session_id, 10)
    db_messages.reverse()
    messages = []
    for message in db_messages:
        if message.user_id != None:
            messages.append(HumanMessage(message.content))
        else:
            messages.append(AIMessage(message.content))
    history.add_messages(messages)
    return history

system_prompt = (
    "Bạn là HealthyHeart Chatbot và bạn đang trò chuyện với khách hàng. "
    "Nhiệm vụ của bạn là tư vấn cho khách hàng về bệnh tim. "
)

bag_of_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("messages"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

# Tools
tools = [heart_predict_tool, faqs_tool, medicine_tool]

agent = create_tool_calling_agent(llm, tools=tools, prompt=bag_of_prompt)
agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=True  # pyright: ignore
)

conversational_agent_executor = RunnableWithMessageHistory(
    agent_executor,  # pyright: ignore
    get_history,
    input_messages_key="messages",
    output_messages_key="output",
)

def chat(pay: CreateMessageModel):
    new_message = conversational_agent_executor.invoke(
        {"messages": [HumanMessage(pay.content)]},
        {"configurable": {"session_id": pay.chat_id}},
    )["output"]

    create_message(
        CreateMessageModel(
            chat_id=pay.chat_id,
            user_id=pay.user_id,
            content=pay.content,
        )
    )

    create_message(
        CreateMessageModel(
            chat_id=pay.chat_id,
            user_id=None,
            content=new_message,
        )
    )

    return new_message
    