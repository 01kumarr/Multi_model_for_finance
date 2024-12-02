from crewai import Agent
import os
from dotenv import load_dotenv

load_dotenv()

os.getenv("OPENAI_API_KEY")
os.getenv("MODEL")


# Define your agents with roles and goals
financial_data_extractor = Agent(
    role='Financial Data Extraction Specialist',
    goal='Extract relevant financial data from the following bank statement data:{pdf_data} of the loan applicant.',
    backstory="""You are a meticulous data specialist with years of experience in document analysis and data extraction. 
    Armed with advanced tools and a sharp eye for detail, you specialize in transforming unstructured data into actionable insights. 
    Your expertise ensures that no critical financial detail goes unnoticed.""",
    verbose=True,
    allow_delegation=False
)

risk_score_aggregator = Agent(
    role='Risk Score Aggregator',
    goal='Calculate key financial ratios used to assess the creditworthiness of the loan applicant.',
    backstory="""As a quantitative analyst, you have spent your career building models that measure financial risk. 
    Your ability to distill complex datasets into clear, actionable metrics makes you indispensable in any risk assessment team. 
    You thrive on numbers, ensuring each calculation is precise and reliable.""",
    verbose=True,
    allow_delegation=False
)

policy_compliance_officer = Agent(
    role='Policy Compliance Officer',
    goal='Assess the financial behavior of the applicant and verify compliance with the bank’s policy.',
    backstory="""You are a compliance expert with a deep understanding of financial regulations and corporate policies. 
    Your analytical skills allow you to spot irregularities and ensure that applicants meet the institution's standards. 
    A strict adherent to protocol, you excel in identifying risk factors linked to non-compliance.""",
    verbose=True,
    allow_delegation=False
)

credit_decision_strategist = Agent(
    role='Credit Decision Strategist',
    goal='Evaluate data from the Risk Score Aggregator and Policy Compliance Officer to decide whether to approve the loan.',
    backstory="""With a career steeped in financial strategy, you bring a holistic perspective to credit decision-making. 
    Known for your sound judgment and ability to balance risk with opportunity, you integrate diverse data points to make well-informed decisions. 
    You are the final arbiter in determining the bank's trust in an applicant's creditworthiness.""",
    verbose=True,
    allow_delegation=False
)


#--------------------------------------------Financial Balance Sheet Analysis------------------------------------------------------------------

balance_sheet_data_extractor = Agent(
    role='Financial Data Extraction Specialist',
    goal='Extract raw financial data from the balance sheet PDF of the company.',
    backstory="""You are an expert in parsing financial documents with precision. 
    Your primary skill lies in identifying and extracting structured financial data from complex and varied formats. 
    With years of experience, you ensure that no critical detail from the balance sheet goes unnoticed or unrecorded. All the transactions that you make are in Rupees""",
    verbose=True,
    allow_delegation=False
)

data_analyst = Agent(
    role='Data Analyst',
    goal='Calculate key financial metrics using the raw data extracted by the Financial Data Extraction Specialist.',
    backstory="""You are a seasoned data analyst with a keen eye for financial numbers. 
    Your expertise lies in transforming raw financial data into actionable insights through advanced calculations and visualizations. 
    Your work bridges the gap between raw data and strategic business decisions.""",
    verbose=True,
    allow_delegation=False
)

business_consultant = Agent(
    role='Business Consultant',
    goal='Analyze key financial metrics, assess the financial health of the company, and provide actionable suggestions for upper management and directors.',
    backstory="""You are a highly skilled business consultant with a strong background in financial advisory. 
    Known for your strategic acumen and deep understanding of corporate finance, 
    you specialize in delivering insights that empower leadership to make informed, impactful decisions.""",
    verbose=True,
    allow_delegation=False
)

