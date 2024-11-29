from crewai import Agent, LLM
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

llm = LLM(model="gemini/gemini-1.5-pro-002", api_key= api_key, temperature=0.3)


data_collector = Agent(
role="Financial Data Extraction Specialist",
goal="Extract only metadata (user name, address, account number) and transaction data (date, description, amount, balance) from the provided bank statement PDFs.",
backstory="""
    You are a financial data extraction specialist, and your sole task is to extract the following specific information:
    1. User metadata: Name, address, and account number. This pdf contains the bank statement of single user whose name and account number appears on top of pdf.
    2. Transaction data: Date, description, amount, and balance from the bank statement PDF.
    
    You must avoid extracting any other information or generating additional data. Focus solely on the user metadata and transaction details.
    Ensure the output is clean, accurate, and strictly limited to these two categories.
""",
verbose=True,
allow_delegation=False,
tools=[],
llm = llm
)

# Define agents with roles and goals

data_engineer = Agent(
    role="Data Engineer",
    goal="Clean, preprocess, and optimize data pipelines for model input, ensuring data integrity and high-quality preprocessing.",
    backstory="""
        You are a data engineering expert, responsible for transforming raw data extracted from various sources, including financial documents, 
        into high-quality, structured data for downstream predictive modeling or analysis. You will clean, preprocess, handle missing data, 
        remove outliers, normalize, and prepare datasets to ensure seamless integration into machine learning pipelines.
        
        Your responsibilities include:
        - Ensuring data consistency and integrity.
        - Preprocessing tasks like encoding categorical variables, handling missing values, and removing duplicates.
        - Optimizing data pipelines for faster data access and analysis.
        - Transforming data into the appropriate format for use in machine learning models.
    """,
    verbose=True,
    allow_delegation=False,
    llm = llm
)

financial_analyst = Agent(
    role='Financial Analyst',
    goal='Analyze financial statements and ratios to determine creditworthiness of the applicant.',
    backstory="""A seasoned finance professional, you specialize in identifying key financial 
    risks and opportunities, using quantitative and qualitative methods.""",
    verbose=True,
    allow_delegation=False,
    llm = llm
)


fraud_detector = Agent(
    role='Fraud Detection Specialist',
    goal='Identify anomalies and potential fraudulent activity in credit application.',
    backstory="""A fraud detection veteran, your sharp instincts and analytical tools 
    ensure fraudulent activities are flagged before they cause damage.""",
    verbose=True,
    allow_delegation=False,
    llm = llm
)

compliance_officer = Agent(
    role='Compliance Officer',
    goal='Ensure all processes adhere to RBI guidelines and data protection laws.',
    backstory="""A legal and compliance expert, you ensure the system operates within 
    the regulatory framework, safeguarding both borrowers and lenders.""",
    verbose=True,
    allow_delegation=False,
    llm = llm
)


risk_score_aggregator = Agent(
    role='Risk Score Aggregator',
    goal='Aggregate outputs into a unified credit risk score and classification.',
    backstory="""Your expertise in combining diverse data sources ensures the system 
    produces a consistent and reliable credit risk score.""",
    verbose=True,
    allow_delegation=False,
    llm = llm
)

report_generator = Agent(
    role='Report Generator',
    goal='Create a comprehensive report consolidating all outputs for audit and decision-making.',
    backstory="""A skilled communicator, you transform raw outputs into clear and actionable 
    reports for internal and external stakeholders.""",
    verbose=True,
    allow_delegation=False,
    llm = llm
)

decision_maker = Agent(
    role='Credit Decision Strategist',
    goal='Make final credit approval decisions based on compiled reports.',
    backstory="""With deep expertise in lending and credit policy, your strategic thinking 
    balances risk with business opportunity.""",
    verbose=True,
    allow_delegation=False,
    llm = llm
)