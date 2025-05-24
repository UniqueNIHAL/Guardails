# In your project folder, create test_groq.py:
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()
llm = ChatGroq(
    model_name="llama3-70b-8192",
    api_key=os.environ["GROQ_API_KEY"],
    temperature=0.7
)
response = llm.invoke("Tell me a fun fact about computers.")
print(response.content if hasattr(response, "content") else str(response))
