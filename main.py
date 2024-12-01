import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import os
from src.crew import *


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

# API 1: Accept JSON and PDF file
@app.post("/upload")
async def upload_files(pdf_file: UploadFile):

    pdf_path = os.path.join(UPLOAD_DIRECTORY, pdf_file.filename)
    with open(pdf_path, "wb") as f:
        f.write(await pdf_file.read())
    
    # Pass file locations to the function
    return fin_crew(pdf_path)

@app.post("/upload_org")
async def upload_files_org(pdf_file: UploadFile):

    pdf_path = os.path.join(UPLOAD_DIRECTORY, pdf_file.filename)
    with open(pdf_path, "wb") as f:
        f.write(await pdf_file.read())
    
    # Pass file locations to the function
    return fin_org_crew(pdf_path)


# @app.get("/get-output/")
# async def get_output():
#     # Check if the output file exists
#     if os.path.exists(OUTPUT_FILE_PATH):
#         with open(OUTPUT_FILE_PATH, "r") as output_file:
#             content = output_file.read()
#         return {"output": content}
#     else:
#         return {"error": "No output file found. Ensure the workflow has been executed."}


if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)