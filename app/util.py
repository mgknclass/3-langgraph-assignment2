from langchain_openai import ChatOpenAI
from app.config import settings

llm = ChatOpenAI(
    api_key=settings.openai_api_key, model=settings.llm_model_name, temperature=0
)
