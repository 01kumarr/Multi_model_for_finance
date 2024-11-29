from crewai import Crew, Process
from agents import *
from tasks import *
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
# os.getenv("MODEL")    


def fin_crew(pdf_p):



    # Initialize a Crew for the Credit Risk Assessment Workflow
    credit_risk_crew = Crew(
        agents=[
            data_collector,
            data_engineer,
            financial_analyst,
            fraud_detector,
            compliance_officer,
            risk_score_aggregator,
            report_generator,
            decision_maker
        ],
        tasks=[
            data_collector_task,
            data_engineer_task,
            financial_analyst_task,
            fraud_detector_task,
            compliance_officer_task,
            risk_score_aggregator_task,
            report_generator_task,
            decision_maker_task
        ],
        process=Process.sequential,
        memory=True,
        embedder={
        "provider": "google",
        "config": {
            "api_key": api_key,
            "model": 'models/embedding-001'
            }
        },
        verbose=True
    )


    # Kick off the workflow
    agent_result= credit_risk_crew.kickoff()

    agent_output = {}
    agent_output["final_answer"] = agent_result.raw
    agent_output["agents"] = []
    for tas in agent_result.tasks_output:
        agent_output["agents"].append({"agentName" : tas.agent, "agentResponse" : tas.raw})


    return agent_output

fin_crew("C:\\Users\\Microsoft\\Desktop\\AI-Agent\\uploaded_files\\Financial-Examples-for-I20.pdf")