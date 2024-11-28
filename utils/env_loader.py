from dotenv import load_dotenv
import os
def load_environment_variables():
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is not set in .env file.")