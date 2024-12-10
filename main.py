import uvicorn
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import os
from langsmith import traceable
from dotenv import load_dotenv
from src.crew import *
from src.vinit import *

# Load environment variables
load_dotenv()

# LangSmith Configuration
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2") == "true"
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
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

@traceable  # Enable LangSmith tracing for this function
def traced_fin_crew(pdf_path: str, text: str):
    """
    Wrapper for fin_crew function to enable LangSmith tracing.
    """
    return fin_crew(pdf_path, text)

@traceable  # Enable LangSmith tracing for this function
def traced_default_chat_vinit(text: str):
    """
    Wrapper for default_chat_vinit function to enable LangSmith tracing.
    """
    return default_chat_vinit(text)

@traceable  # Enable LangSmith tracing for this function
def traced_fin_org_crew(pdf_path: str, text: str):
    """
    Wrapper for fin_org_crew function to enable LangSmith tracing.
    """
    return fin_org_crew(pdf_path, text)

# API 1: Accept JSON and PDF file
@app.post("/upload")
async def upload_files(pdf_file: UploadFile = None, text: str = Form(None)):
    """
    Endpoint to handle text or file uploads and process them.
    """
    if pdf_file is not None:
        pdf_path = os.path.join(UPLOAD_DIRECTORY, pdf_file.filename)
        with open(pdf_path, "wb") as f:
            f.write(await pdf_file.read())

        # Pass file locations to the traced function
        return traced_fin_crew(pdf_path, text)
    else:
        return traced_default_chat_vinit(text)

@app.post("/upload_org")
async def upload_files_org(pdf_file: UploadFile = None, text: str = Form(None)):
    """
    Endpoint to handle organization-specific uploads.
    """
    if pdf_file is not None and text:
        pdf_path = os.path.join(UPLOAD_DIRECTORY, pdf_file.filename)
        with open(pdf_path, "wb") as f:
            f.write(await pdf_file.read())

        # Pass file locations to the traced function
        return traced_fin_org_crew(pdf_path, text)
    else:
        return traced_default_chat_vinit(text)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
