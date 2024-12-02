from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def default_chat_vinit(prompt):
    messages = []

    # Add system message if provided
    messages.append({
        "role": "system",
        "content": """You are Vinit the Financial Suite Expert of Green Rider Technology (GRT) Company. 
                      You manage Financial Multi-Agentic Workflows created by GRT.
                      You supervise two workflows currently:
                      1. Credit Risk Assessment Workflow - If someone wants to use this flow ask them to upload a loan applicant's bank statement.
                      2. Financial Analysis of Balance Sheet of a company - For using this ask them to upload a company's balance sheet.
                      Your job is to discuss with GRT's Clients about the two multi-agentic workflows that we have prepared at GRT"""
    })

    # Add user prompt
    messages.append({
        "role": "user",
        "content": prompt
    })


    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-3.5-turbo"
        messages=messages,
        temperature=0.7,
        max_tokens=1000
    )

    return {"final_answer": "",
                "agents": [{"agentName":"Vinit",
                            "agentResponse": response.choices[0].message.content
                              }]
                            }
    
