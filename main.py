import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from nemoguardrails import RailsConfig, LLMRails
from langchain_groq import ChatGroq
import uvicorn

load_dotenv()

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

try:
    # Initialize with guardrails
    llm = ChatGroq(
        model_name="llama3-70b-8192",
        api_key=os.environ["GROQ_API_KEY"],
        temperature=0.7
    )
    config = RailsConfig.from_path("./config")
    rails = LLMRails(config, llm=llm)

except Exception as e:
    print(f"Initialization error: {str(e)}")
    raise

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        context = await rails.generate_async(prompt=request.message)
        return {"response": context}
    except Exception as e:
        return {"response": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)