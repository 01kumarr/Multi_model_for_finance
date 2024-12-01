from crewai import Crew, Process
from crewai_tools import PDFSearchTool
from src.agents import *
from src.tasks import *
from PyPDF2 import PdfReader
import pdfplumber
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
os.getenv("GOOGLE_API_KEY")
os.getenv("MODEL")

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    return text



def extract_tables_from_pdf(pdf_path):
    # Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        # Initialize an empty list to store all tables
        all_tables = []
        
        # Iterate through each page
        for page in pdf.pages:
            # Extract tables from the current page
            tables = page.extract_tables()
            
            # Add tables to our list if any were found
            if tables:
                all_tables.extend(tables)
    
    # Convert tables to pandas DataFrames and store them
    dfs = []
    for i, table in enumerate(all_tables):
        df = pd.DataFrame(table[1:], columns=table[0])  # Assuming first row contains headers
        dfs.append(df)
        
        # Optionally save each table to CSV
        df.to_csv(f'table_{i+1}.csv', index=False)





def fin_crew(pdf_p):
    
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
        'pdf_data': pdf_d
    }


    # Kick off the workflow
    agent_result= credit_risk_assessment_crew.kickoff(inputs=inputs)

    agent_output = {}
    agent_output["final_answer"] = agent_result.raw
    agent_output["agents"] = []
    for tas in agent_result.tasks_output:
        agent_output["agents"].append({"agentName" : tas.agent, "agentResponse" : tas.raw})


    return agent_output

#fin_crew("C:\\Users\\Admin\\Desktop\\AI-Agent\\uploaded_files\\Financial-Examples-for-I20.pdf")