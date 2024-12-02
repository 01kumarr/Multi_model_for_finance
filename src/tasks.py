from src.agents import *
from crewai import Task

# Create tasks for your agents
financial_data_extractor_task = Task(
    description="""Here is the bank statement data of the loan applicant: {pdf_data}

    Using the bank statement data extract the name, account number of the applicant and the following critical financial data points:
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
    - Total Monthly Debt Payments (Note: If you are not able to find any debt data then consider it as 0)
    - Gross Monthly Income
    - Sum of Daily Balances
    - Number of Days
    - Lowest Monthly Income
    - Highest Monthly Income
    - Total Credits
    - Total Debits
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
    - Name of Applicant
    - Calculated ratios: DTI, Income Stability, Average Daily Balance, Income to Outflow
    - Loan approval Advice for the applicant considering the ratios in bullet points.
    - Reasons for decision: [Bullet point list of reasons based on ratio values]
    """,
    agent=risk_score_aggregator
)

policy_compliance_officer_task = Task(
    description="""Here is the bank statement data of the loan applicant: {pdf_data}
    
    Using the bank statement data analyze the applicant's financial behavior.
    Check for the following:
    1. Regular salary credits
    2. Bounce/return charges
    3. Consistent bill payments
    4. Large unexplained transactions
    Provide a summary of key financial behavior insights, focusing on income stability, cash management skills, payment behavior, and overall financial health.""",
    expected_output="""A compliance report including:
    - Key insights (listed in bullet points): [Income stability, Cash management skills, Payment behavior, Overall financial health]
    - Specific observations for each behavior check: [Details of findings in bullet points]
    """,
    agent=policy_compliance_officer
)

credit_decision_strategist_task = Task(
    description="""Evaluate the data and insights provided by the Risk Score Aggregator and Policy Compliance Officer.
    Synthesize findings to decide whether the applicant's loan can be approved, ensuring the decision is justified by:
    - The calculated financial ratios
    - Observations on the applicant's financial behavior
    Provide a detailed decision report listing all points and reasons considered in making the decision.""",
    expected_output="""A comprehensive credit decision report for [Name of Applicant] including:
    - Decision: [Approved/Denied]
    - Supporting points: [Bullet point of factors considered from financial ratios and behavior analysis]
    - Justification: [Detailed reasoning in bullet points for the decision]
    Also provide answer for this {query}
    """,
    agent=credit_decision_strategist,
    context=[risk_score_aggregator_task]
)



#--------------------------------------------Financial Balance Sheet Analysis------------------------------------------------------------------


# Create tasks for your agents
balance_sheet_data_extractor_task = Task(
    description="""Here is the company's balance sheet data: {pdf_data1}

    Using the balance sheet data extract the following critical financial data points:
    1. Current Assets
    2. Current Liabilities
    3. Total Liabilities
    4. Shareholders' Equity
    5. Net Income
    6. Revenue
    7. Total Assets
    8. Fixed Assets
    9. EBIT
    10. Total Debt Service
    11. Cost of Goods Sold (COGS)
    12. Average Inventory
    13. Cash and Cash Equivalents
    14. Marketable Securities
    15. Current Liabilities
    16. Total Outstanding Shares
    Structure the extracted data in a format suitable for subsequent analysis.""",
    expected_output="""A structured dataset including:
    - Current Assets
    - Current Liabilities
    - Total Liabilities
    - Shareholders' Equity
    - Net Income
    - Revenue
    - Total Assets
    - Fixed Assets
    - EBIT
    - Total Debt Service
    - Cost of Goods Sold (COGS)
    - Average Inventory: [Value]
    - Cash and Cash Equivalents
    - Marketable Securities
    - Current Liabilities
    - Total Outstanding Shares
    """,
    agent=balance_sheet_data_extractor
)

data_analyst_task = Task(
    description="""Using the extracted financial data, calculate the following financial metrics:
    1. Current Ratio = Current Assets / Current Liabilities
    2. Debt-to-Equity Ratio = Total Liabilities / Shareholders' Equity
    3. Net Working Capital = Current Assets - Current Liabilities
    4. Return on Equity (ROE) = Net Income / Shareholders' Equity
    5. Asset Turnover Ratio = Revenue / Total Assets
    6. Fixed Asset Turnover Ratio = Revenue / Fixed Assets
    7. Debt Service Coverage Ratio (DSCR) = EBIT / Total Debt Service
    8. Inventory Turnover Ratio = Cost of Goods Sold (COGS) / Average Inventory
    9. Cash Ratio = (Cash and Cash Equivalents + Marketable Securities) / Current Liabilities
    10. Book Value per Share = Shareholders' Equity / Total Outstanding Shares
    Provide insights into the calculated metrics, highlighting any positive trends or potential financial concerns.""",
    expected_output="""A report including:
    - Calculated metrics with values for:
      Current Ratio, Debt-to-Equity Ratio, Net Working Capital, ROE, Asset Turnover Ratio,
      Fixed Asset Turnover Ratio, DSCR, Inventory Turnover Ratio, Cash Ratio, Book Value per Share.
    - Insights for each metrics should also be included citing if they have Positive trends or Potential problems.
    """,
    agent=data_analyst
)

business_consultant_task = Task(
    description="""Analyze the report provided by the Data Analyst, including the calculated metrics and insights.
    Provide an assessment of the company’s financial health, including strengths, weaknesses, and areas of concern.
    Suggest actionable recommendations for the upper management and directors to improve the company’s financial standing.
    The recommendations should be specific and implementable, focusing on enhancing financial performance and mitigating risks.""",
    expected_output="""A consultancy report including:
    - Financial health assessment: [Overview of strengths, weaknesses, and concerns]
    - Recommendations: [Actionable steps for improvement]
    - Strategic advice: [Long-term strategies for financial stability and growth]
    Also provide answer for this {query}
    """,
    agent=business_consultant
)