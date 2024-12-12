import requests
from langsmith import traceable
from dotenv import load_dotenv
import os 

# Load environment variables
load_dotenv()

# LangSmith Configuration
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2") == "true"
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")

# FastAPI application URL
BASE_URL = "http://127.0.0.1:8000"

@traceable  # Enable LangSmith tracing for this function
def process_crewai_request(endpoint: str, pdf_file_path: str = None, text: str = None):
    """
    Send a request to the crewai FastAPI server and trace the interaction.
    """
    files = {"pdf_file": open(pdf_file_path, "rb")} if pdf_file_path else {}
    data = {"text": text} if text else {}

    try:
        response = requests.post(f"{BASE_URL}/{endpoint}", files=files, data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@traceable  # Trace the overall pipeline
def pipeline(user_input: str, pdf_file_path: str = None):
    """
    Process input through the crewai FastAPI endpoints and log with LangSmith.
    """
    if pdf_file_path:
        return process_crewai_request("upload", pdf_file_path=pdf_file_path, text=user_input)
    else:
        return process_crewai_request("upload", text=user_input)

# Optional test block
if __name__ == "__main__":
    print("Testing integration scripts...")

    # Test Example: Send text input
    result_text = pipeline("Hello from integration script")
    print("Text Input Response:", result_text)

    # Test Example: Send a PDF file
    pdf_path = "example.pdf"  # Replace with an actual file
    try:
        result_pdf = pipeline("Processing the PDF", pdf_file_path=pdf_path)
        print("PDF Input Response:", result_pdf)
    except FileNotFoundError:
        print("PDF file not found. Ensure 'example.pdf' exists.")
