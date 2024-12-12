from fastapi import FastAPI, UploadFile, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import uuid
from langsmith import traceable
from dotenv import load_dotenv
from src.crew import *
from src.vinit import *
from typing import Dict

# Load environment variables
load_dotenv()

# LangSmith Configuration
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2") == "true"
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")

# FastAPI app initialization
app = FastAPI(
    title="Credit Risk Assessment Agent Flow AI APIs",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory to save uploaded files
UPLOAD_DIRECTORY = "uploaded_files"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# Simulated database for tracking tasks
tasks: Dict[str, Dict] = {}

@traceable
def traced_fin_crew(pdf_path: str, text: str):
    return fin_crew(pdf_path, text)

@traceable
def traced_default_chat_vinit(text: str):
    return default_chat_vinit(text)

@traceable
def traced_fin_org_crew(pdf_path: str, text: str):
    return fin_org_crew(pdf_path, text)

def process_pdf_task(task_id: str, pdf_path: str, text: str):
    """
    Process PDF and update task status.
    """
    try:
        # Call the traced_fin_crew function to process the PDF
        result = traced_fin_crew(pdf_path, text)
        tasks[task_id]["status"] = "completed"
        tasks[task_id]["result"] = result
    except Exception as e:
        # Handle any errors during processing
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["result"] = str(e)



@app.post("/upload")
async def upload_files(
    pdf_file: UploadFile = None,
    text: str = Form(None),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    if pdf_file is not None:
        # Save the PDF file
        pdf_path = os.path.join(UPLOAD_DIRECTORY, pdf_file.filename)
        with open(pdf_path, "wb") as f:
            f.write(await pdf_file.read())
        
        # Generate a task ID
        task_id = str(uuid.uuid4())
        tasks[task_id] = {"status": "processing", "result": None}

        # Start processing in the background
        background_tasks.add_task(process_pdf_task, task_id, pdf_path, text)

        return JSONResponse(
            content={
                "message": (
                    "Your file has been received and is being processed. "
                    "In the meantime, feel free to ask financial-related queries."
                ),
                "task_id": task_id
            },
            status_code=202
        )
    elif text:
        # Process text query immediately
        response = traced_default_chat_vinit(text)
        return JSONResponse(content=response)
    else:
        return JSONResponse(content={"error": "No input provided"}, status_code=400)

@app.get("/task_status/{task_id}")
async def get_task_status(task_id: str):
    """
    Endpoint to check the status of a PDF processing task.
    """
    task = tasks.get(task_id)
    if not task:
        return JSONResponse(content={"error": "Task not found"}, status_code=404)

    return JSONResponse(content=task)

@app.post("/upload_org")
async def upload_files_org(
    pdf_file: UploadFile = None,
    text: str = Form(None),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    if pdf_file is not None:
        # Save the PDF file
        pdf_path = os.path.join(UPLOAD_DIRECTORY, pdf_file.filename)
        with open(pdf_path, "wb") as f:
            f.write(await pdf_file.read())
        
        # Generate a task ID
        task_id = str(uuid.uuid4())
        tasks[task_id] = {"status": "processing", "result": None}

        # Start processing in the background
        background_tasks.add_task(process_pdf_task, task_id, pdf_path, text)

        return JSONResponse(
            content={
                "message": (
                    "Your file has been received and is being processed. "
                    "In the meantime, feel free to ask financial-related queries."
                ),
                "task_id": task_id
            },
            status_code=202
        )
    elif text:
        # Process text query immediately
        response = traced_default_chat_vinit(text)
        return JSONResponse(content=response)
    else:
        return JSONResponse(content={"error": "No input provided"}, status_code=400)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
