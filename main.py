from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import os
from src.crew import fin_crew


# FastAPI app initialization
app = FastAPI(
    title="Credit Risk Assessment Agent Flow AI APIs",
    version="1.0.0"
    )

origins = [
    "http://localhost",
    "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory to save uploaded files
UPLOAD_DIRECTORY = "uploaded_files"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# API 1: Accept JSON and PDF file
@app.post("/upload/")
async def upload_files(pdf_file: UploadFile):
    # Save JSON file
    # json_path = os.path.join(UPLOAD_DIRECTORY, json_file.filename)
    # with open(json_path, "wb") as f:
    #     f.write(await json_file.read())

    # Validate JSON content
    # with open(json_path, "r") as f:
    #     try:
    #         data = json.load(f)
    #     except json.JSONDecodeError:
    #         return {"error": "Invalid JSON file"}

    # Save PDF file
    pdf_path = os.path.join(UPLOAD_DIRECTORY, pdf_file.filename)
    with open(pdf_path, "wb") as f:
        f.write(await pdf_file.read())

    # Pass file locations to the function
    return fin_crew(pdf_path)



# @app.get("/get-output/")
# async def get_output():
#     # Check if the output file exists
#     if os.path.exists(OUTPUT_FILE_PATH):
#         with open(OUTPUT_FILE_PATH, "r") as output_file:
#             content = output_file.read()
#         return {"output": content}
#     else:
#         return {"error": "No output file found. Ensure the workflow has been executed."}