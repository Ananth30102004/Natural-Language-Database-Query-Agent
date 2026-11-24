from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from messages import ask_datapilot,Create_Agent
from contextlib import asynccontextmanager
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Starting DataPilot...")

    agent = await Create_Agent()

    app.state.agent = agent

    print("DataPilot agent initialized!")

    yield

    print("Shutting down DataPilot...")

app = FastAPI(lifespan=lifespan)

class request(BaseModel):
    question:str

@app.get("/")

def home():
    return {"message" : "Welcome to Datapilot"}

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application" : "Datapilot"
    }

@app.post("/ask")
async def ask_qn (request:request):

    try:
        agent = app.state.agent
        answer =await ask_datapilot(agent, request.question)
        return{
            "received_question" : request.question,
            "answer" : answer 
        }

    except Exception as e:
        import traceback

        print("\n--- DATAPILOT ERROR ---")
        traceback.print_exc()

        raise HTTPException(
            status_code=503,
            detail="DataPilot AI service is temporarily unavailable."
        )