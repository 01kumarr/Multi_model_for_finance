from crewai import Crew
from src.agents import *
from src.tasks import *
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv

load_dotenv()
os.getenv("OPENAI_API_KEY")
os.getenv("MODEL")

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    return text



def fin_crew(pdf_p, query):
    
    #data_collector.tools.append(pdf_search_tool)

    # Initialize a Crew for the Credit Risk Assessment Workflow
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


    # Extract tables
    pdf_d = extract_text_from_pdf(pdf_p)

    inputs = {
        'pdf_data': pdf_d,
        'query': query
    }


    # Kick off the workflow
    agent_result= credit_risk_assessment_crew.kickoff(inputs=inputs)

    agent_output = {}
    agent_output["final_answer"] = agent_result.raw
    agent_output["agents"] = []
    for tas in agent_result.tasks_output:
        agent_output["agents"].append({"agentName" : tas.agent, "agentResponse" : tas.raw})


    return agent_output


def fin_org_crew(pdf_p1, query):
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

    pdf_d1 = extract_text_from_pdf(pdf_p1)

    inputs1 = {
        'pdf_data1': pdf_d1,
        'query': query
    }


    # Kick off the workflow
    agent_result1= strategic_balance_analyzer_crew.kickoff(inputs=inputs1)

    agent_output1 = {}
    agent_output1["final_answer"] = agent_result1.raw
    agent_output1["agents"] = []
    for tas in agent_result1.tasks_output:
        agent_output1["agents"].append({"agentName" : tas.agent, "agentResponse" : tas.raw})


    return agent_output1


