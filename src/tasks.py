from src.agents import *
from crewai import Task

# Create tasks for your agents
financial_data_extractor_task = Task(
    description="""Extract the following critical financial data points from {pdf_data}:
    1. Total Monthly Debt Payments
    2. Gross Monthly Income
    3. Sum of Daily Balances
    4. Number of Days (in the statement period)
    5. Lowest Monthly Income
    6. Highest Monthly Income
    7. Total Credits
    8. Total Debits
    These data points must be structured and presented in a format suitable for subsequent financial ratio calculations.""",
    expected_output="""A structured dataset including:
    - Total Monthly Debt Payments: [Value]
    - Gross Monthly Income: [Value]
    - Sum of Daily Balances: [Value]
    - Number of Days: [Value]
    - Lowest Monthly Income: [Value]
    - Highest Monthly Income: [Value]
    - Total Credits: [Value]
    - Total Debits: [Value]
    """,
    agent=financial_data_extractor
)

risk_score_aggregator_task = Task(
    description="""Using the extracted financial data, calculate the following financial ratios:
    1. Debt-to-Income (DTI) Ratio = Total Monthly Debt Payments / Gross Monthly Income
    2. Income Stability Ratio = Lowest Monthly Income / Highest Monthly Income
    3. Average Daily Balance Ratio = Sum of Daily Balances / Number of Days
    4. Income to Outflow Ratio = Gross Monthly Income / Total Debits
    Provide an assessment of whether the loan can be approved based on these ratios, along with a detailed list of reasons derived from the analysis.""",
    expected_output="""A report including:
    - Calculated ratios: DTI, Income Stability, Average Daily Balance, Income to Outflow
    - Loan approval status: [Approved/Denied]
    - Reasons for decision: [List of reasons based on ratio values]
    """,
    agent=risk_score_aggregator
)

policy_compliance_officer_task = Task(
    description="""Analyze the applicant's financial behavior using the bank statement data from {pdf_data} to check for:
    1. Regular salary credits
    2. Bounce/return charges
    3. Consistent bill payments
    4. Large unexplained transactions
    Provide a summary of key financial behavior insights, focusing on income stability, cash management skills, payment behavior, and overall financial health.""",
    expected_output="""A compliance report including:
    - Key insights: [Income stability, Cash management skills, Payment behavior, Overall financial health]
    - Specific observations for each behavior check: [Details of findings]
    """,
    agent=policy_compliance_officer
)

credit_decision_strategist_task = Task(
    description="""Evaluate the data and insights provided by the Risk Score Aggregator and Policy Compliance Officer.
    Synthesize findings to decide whether the applicant's loan can be approved, ensuring the decision is justified by:
    - The calculated financial ratios
    - Observations on the applicant's financial behavior
    Provide a detailed decision report listing all points and reasons considered in making the decision.""",
    expected_output="""A comprehensive credit decision report including:
    - Decision: [Approved/Denied]
    - Supporting points: [List of factors considered from financial ratios and behavior analysis]
    - Justification: [Detailed reasoning for the decision]
    """,
    agent=credit_decision_strategist,
    context=[risk_score_aggregator_task]
)
