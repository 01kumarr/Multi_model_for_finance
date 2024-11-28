from crewai import Agent, Task, Crew, Process
from crewai_tools import PDFSearchTool
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
os.getenv("OPENAI_API_KEY")
os.getenv("MODEL")


def fin_crew(pdf_p):
    llm = ChatOpenAI(
    model='gpt-4',
    temperature=0.3
    )

    # File storage paths (ensure these directories exist)
    #JSON_STORAGE_PATH = json_p
    PDF_STORAGE_PATH = pdf_p
    #OUTPUT_FILE_PATH = "C:/Users/Admin/Desktop/MyMandi Customer Support/mymandi_customer_support/src/mymandi_customer_support/data/credit_report.md"  # Path to store the final output report

    # Define tools with placeholder paths (updated dynamically during runtime)
    #json_tool = JSONSearchTool(json_path=JSON_STORAGE_PATH)
    pdf_search_tool = PDFSearchTool(pdf=PDF_STORAGE_PATH)

    # Define agents with roles and goals
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
    tools=[pdf_search_tool],
    llm = llm
    )

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
    )

    financial_analyst = Agent(
        role='Financial Analyst',
        goal='Analyze financial statements and ratios to determine creditworthiness of the applicant.',
        backstory="""A seasoned finance professional, you specialize in identifying key financial 
        risks and opportunities, using quantitative and qualitative methods.""",
        verbose=True,
        allow_delegation=True
    )


    fraud_detector = Agent(
        role='Fraud Detection Specialist',
        goal='Identify anomalies and potential fraudulent activity in credit application.',
        backstory="""A fraud detection veteran, your sharp instincts and analytical tools 
        ensure fraudulent activities are flagged before they cause damage.""",
        verbose=True,
        allow_delegation=False
    )

    compliance_officer = Agent(
        role='Compliance Officer',
        goal='Ensure all processes adhere to RBI guidelines and data protection laws.',
        backstory="""A legal and compliance expert, you ensure the system operates within 
        the regulatory framework, safeguarding both borrowers and lenders.""",
        verbose=True,
        allow_delegation=False
    )


    risk_score_aggregator = Agent(
        role='Risk Score Aggregator',
        goal='Aggregate outputs into a unified credit risk score and classification.',
        backstory="""Your expertise in combining diverse data sources ensures the system 
        produces a consistent and reliable credit risk score.""",
        verbose=True,
        allow_delegation=False
    )

    report_generator = Agent(
        role='Report Generator',
        goal='Create a comprehensive report consolidating all outputs for audit and decision-making.',
        backstory="""A skilled communicator, you transform raw outputs into clear and actionable 
        reports for internal and external stakeholders.""",
        verbose=True,
        allow_delegation=False
    )

    decision_maker = Agent(
        role='Credit Decision Strategist',
        goal='Make final credit approval decisions based on compiled reports.',
        backstory="""With deep expertise in lending and credit policy, your strategic thinking 
        balances risk with business opportunity.""",
        verbose=True,
        allow_delegation=True
    )

    # Define tasks for each agent with expected outputs
    data_collector_task = Task(
        description="Extract metadata and transaction data from the provided PDF.",
        agent=data_collector,
        expected_output="""{
            "metadata": {"name": "John Doe", "address": "123 Example Street", "account_number": "9876543210"},
            "Transaction Data":
            1. Date: 09 Sep 2024, Description: TRANSFER TO 4897691162095 - UPI/DR/461955486080/LALTESH /YESB/q225242534/NA, Amount: 40.00, Balance: 8206.13
            2. Date: 10 Sep 2024, Description: TRANSFER TO 4897692162094 - UPI/DR/425492172515/Bank Acc/BARB/5258810001/Payme, Amount: 5000.00, Balance: 3206.13
            3. Date: 10 Sep 2024, Description: TRANSFER TO 4897692162094 - UPI/DR/462006262116/AYUSHMAAN/ PUNB/8171549969/Paym, Amount: 220.00, Balance: 2986.13
            4. Date: 10 Sep 2024, Description: TRANSFER TO 4897692162094 - UPI/DR/462089731258/Ritik K/SBIN/9135947482/Payme, Amount: 1000.00, Balance: 1986.13
            5. Date: 10 Sep 2024, Description: TRANSFER TO 4897692162094 - UPI/DR/425497241124/ASTROTAL/AI RP/panditji36/Pandi, Amount: 29.50, Balance: 1956.63
            6. Date: 11 Sep 2024, Description: TRANSFER TO 4897693162093 - UPI/DR/425517810472/Jayram /SBIN/jayrampal7/Sent, Amount: 40.00, Balance: 1916.63
                    ]
        }"""
    )

    data_engineer_task = Task(
        description="""Clean, preprocess, and optimize the raw dataset for model input. 
        Ensure consistency, handle missing data, and prepare normalized features. Do not remove any data.""",
        agent=data_engineer,
        expected_output='''
        "User Dataset":

        | Name       | Address                                                                                           | Account_Number |
        |------------|---------------------------------------------------------------------------------------------------|----------------|
        | VIVEK KUMAR| S/O SURESH RAI, VILL/PO-GOTPA,VIA TAKIYA BAZAR SAMITI, PS-SASARAM , ROHTAS, BIHAR, 821115         | 88198964464    |

        Transactions Dataset:

        | Date       | Description                                                                                       | Amount | Balance  |
        |------------|---------------------------------------------------------------------------------------------------|--------|----------|
        | 09 Sep 2024| TRANSFER TO 4897691162095 - UPI/DR/461955486080/LALTESH /YESB/q225242534/NA                       | 40.00  | 8206.13  |
        | 10 Sep 2024| TRANSFER TO 4897692162094 - UPI/DR/425492172515/Bank Acc/BARB/5258810001/Payme                    | 5000.00| 3206.13  |
        | 10 Sep 2024| TRANSFER TO 4897692162094 - UPI/DR/462006262116/AYUSHMAAN/ PUNB/8171549969/Paym                   | 220.00 | 2986.13  |
        | 13 Sep 2024| TRANSFER TO 4897695162091 - UPI/DR/462320562669/GOLAM R/SBIN/9873601441/Sent                      | 40.00  | 1876.63  |
        | 13 Sep 2024| TRANSFER TO 4897695162091 - UPI/DR/462342410051/Delhi Me/YESB/paytm-7949/NA                       | 500.00 | 1376.63  |
        | 15 Sep 2024| ATM CASH 42591 +Rama Park Uttam Nagar Delhi                                                      | 500.00 | 876.63   |
        | 15 Sep 2024| TRANSFER TO                                                                                       | 27.00  | NaN      |
    '''
    )

    financial_analyst_task = Task(
        description="""Analyze financial data, focusing on debt-to-income ratio, 
        credit utilization, and other key metrics. Highlight risk indicators.""",
        agent=financial_analyst,
        expected_output="Financial insights including risk factors, key ratios, and metrics."
    )


    fraud_detector_task = Task(
        description="""Run anomaly detection algorithms to identify fraudulent patterns 
        in credit applications. Flag suspicious cases for further investigation.""",
        agent=fraud_detector,
        expected_output="Fraud flags and insights for suspicious applications."
    )

    compliance_officer_task = Task(
        description="""Review the workflow to ensure compliance with RBI guidelines, 
        data protection laws, and other applicable regulations.""",
        agent=compliance_officer,
        expected_output="Compliance report ensuring regulatory adherence."
    )


    risk_score_aggregator_task = Task(
        description="""Combine financial analysis, fraud detection, and model outputs into 
        a unified credit risk score. Classify applicants into risk tiers (low, medium, high).""",
        agent=risk_score_aggregator,
        expected_output="Unified credit risk score and risk classification."
    )

    report_generator_task = Task(
        description="""Generate a comprehensive report detailing applicant credit scores, 
        financial analysis, and flagged fraud risks. Ensure clarity and completeness.""",
        agent=report_generator,
        expected_output="Consolidated report summarizing all findings and scores."
    )

    decision_maker_task = Task(
        description="""Review the final report and risk scores to make approval or rejection 
        decisions. Ensure decisions align with policy and business goals.""",
        agent=decision_maker,
        expected_output="""
            "Name" : "abc kumar",
            "address" : "xyz",
            "account number" : 12345,
            "Result" : "Accepted or Rejected",
            "Reason" : "due to unfavorable financial ratios – a high Debt-to-Income ratio and a low Quick ratio – suggesting potential 
                difficulty in managing additional debt or impending short-term liabilities..."
        """,
        output_file='credit_report.md'
    )

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