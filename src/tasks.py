from src.agents import *
from crewai import Task

# Define tasks for each agent with expected outputs
data_collector_task = Task(
    description="Extract metadata and transaction data from the provided PDF.",
    agent=data_collector,
    expected_output="""
    Your output should be in the below format do not markdown it as JSON:
    {
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
    Your output should be in the below format:
    User Dataset:

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
    a unified credit risk score. Classify the applicant into risk tiers (low, medium, high).""",
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
        Your output should be in the below format:
        Name : abc kumar
        Address : xyz
        Account number : 12345
        Result : Accepted or Rejected,
        Reason : Due to unfavorable financial ratios – a high Debt-to-Income ratio and a low Quick ratio – suggesting potential 
            difficulty in managing additional debt or impending short-term liabilities...
    """,
    #output_file='credit_report.md'
)