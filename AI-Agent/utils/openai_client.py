import os
from langchain_openai import ChatOpenAI
# Load OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")
chat_openai = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4")
def llm_sentiment_analysis(customer_message):
    response = chat_openai.ChatCompletion.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an empathetic Customer Support Executive analyzing customer sentiment. Your goal is to identify both explicit "
                    "and implicit issues in customer messages, providing a summary that includes sentiment intensity, tone, and main points of concern."
                )
            },
            {"role": "user", "content": f"Analyze the sentiment and summarize main complaints of the customer message: '{customer_message}'"}
        ]
    )
    return response['choices'][0]['message']['content']
def llm_image_validation(image_path):
    """Validates a product image against a reported defect by the customer."""
    response = chat_openai.ChatCompletion.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a Quality Manager responsible for inspecting product images provided by customers. Your goal is to identify visible defects "
                    "and confirm if they match the customer’s complaints.\n\n"
                    "1. **Defect Identification**: Look for visible signs of damage, wear, or malfunction.\n"
                    "2. **Verification**: Determine if the visible issues align with the customer's description.\n"
                    "3. **Inconsistencies**: Note any discrepancies between the image and the description.\n"
                    "4. **Conclusion**: Confirm or deny if the product image validates the complaint."
                )
            },
            {"role": "user", "content": f"Inspect the product image located at '{image_path}' and validate it against the customer’s complaint."}
        ]
    )
    return response['choices'][0]['message']['content']
def llm_refund_calculation(validated_issue):
    response = chat_openai.ChatCompletion.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a Financial Accounts Manager assessing refund amounts based on validated customer complaints. Your role is to determine "
                    "a fair refund amount following company policy.\n\n"
                    "1. **Defect Severity**: Assess the defect’s impact on product usability.\n"
                    "2. **Policy Alignment**: Reference company policies, considering factors like product age, defect severity, and customer history.\n"
                    "3. **Fairness**: Ensure the refund amount is fair to the customer and protects company interests.\n"
                    "4. **Final Recommendation**: Provide a suggested refund amount with a brief justification."
                )
            },
            {"role": "user", "content": f"Determine an appropriate refund based on the following validated issue: '{validated_issue}'"}
        ]
    )
    return response['choices'][0]['message']['content']
def llm_eligibility_review(history):
    response = chat_openai.ChatCompletion.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a Customer Accounts Manager reviewing refund eligibility based on the customer’s history and company policy.\n\n"
                    "1. **Refund History Review**: Examine past refunds for patterns (e.g., frequent minor complaints or substantial refunds).\n"
                    "2. **Policy Compliance**: Cross-reference company policies, noting eligibility criteria.\n"
                    "3. **Risk Assessment**: Assess whether the history suggests potential misuse of the refund policy.\n"
                    "4. **Decision Recommendation**: Recommend eligibility with justification based on policy and risk assessment."
                )
            },
            {"role": "user", "content": f"Considering the customer’s refund history: '{history}', assess their eligibility for a refund."}
        ]
    )
    return response['choices'][0]['message']['content']