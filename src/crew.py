from langsmith import traceable
from PyPDF2 import PdfReader
from crewai import Crew
from src.agents import *
from src.tasks import *
import os 
from dotenv import load_dotenv

load_dotenv()

os.getenv("OPENAI_API_KEY")
os.getenv("MODEL")

@traceable
def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file. Traced for tracking execution in LangSmith.
    """
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


@traceable
def fin_crew(pdf_p, query):
    """
    Credit Risk Assessment workflow with agents and tasks. Traced for LangSmith.
    """
    # Define a crew with agents and tasks
    credit_risk_assessment_crew = Crew(
        agents=[
            financial_data_extractor,
            risk_score_aggregator,
            policy_compliance_officer,
            credit_decision_strategist
        ],
        tasks=[
            financial_data_extractor_task,
            risk_score_aggregator_task,
            policy_compliance_officer_task,
            credit_decision_strategist_task
        ]
    )

    # Extract text from the PDF
    pdf_d = extract_text_from_pdf(pdf_p)

    # Prepare inputs for the crew
    inputs = {
        'pdf_data': pdf_d,
        'query': query
    }

    # Trace kickoff of the workflow
    @traceable
    def kickoff_workflow(crew, inputs):
        return crew.kickoff(inputs=inputs)

    agent_result = kickoff_workflow(credit_risk_assessment_crew, inputs)

    # Build the response
    agent_output = {
        "final_answer": agent_result.raw,
        "agents": [
            {
                "agentName": task.agent,
                "agentResponse": task.raw
            } for task in agent_result.tasks_output
        ]
    }

    return agent_output


@traceable
def fin_org_crew(pdf_p1, query):
    """
    Organizational Analysis workflow with agents and tasks. Traced for LangSmith.
    """
    # Define a crew with agents and tasks
    strategic_balance_analyzer_crew = Crew(
        agents=[
            balance_sheet_data_extractor,
            data_analyst,
            business_consultant
        ],
        tasks=[
            balance_sheet_data_extractor_task,
            data_analyst_task,
            business_consultant_task
        ]
    )

    # Extract text from the PDF
    pdf_d1 = extract_text_from_pdf(pdf_p1)

    # Prepare inputs for the crew
    inputs1 = {
        'pdf_data1': pdf_d1,
        'query': query
    }

    # Trace kickoff of the workflow
    @traceable
    def kickoff_workflow(crew, inputs):
        return crew.kickoff(inputs=inputs)

    agent_result1 = kickoff_workflow(strategic_balance_analyzer_crew, inputs1)

    # Build the response
    agent_output1 = {
        "final_answer": agent_result1.raw,
        "agents": [
            {
                "agentName": task.agent,
                "agentResponse": task.raw
            } for task in agent_result1.tasks_output
        ]
    }

    return agent_output1
