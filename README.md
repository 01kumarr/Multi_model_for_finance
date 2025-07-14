# AI-Powered Credit Risk Assessment System
This project automates credit risk assessment using CrewAI agents, enabling intelligent and interpretable decisions based on unstructured financial documents (PDF bank statements). It simulates an underwriting team with defined roles using an agentic workflow.

```AI-Agent/
├── db/
├── uploaded_files/              # Folder for input bank statement PDFs
├── src/
│   ├── __init__.py
│   ├── agents.py                # Defines CrewAI agents with specific roles and goals
│   ├── crew.py                  # Initializes the Crew and executes the workflow
│   ├── tasks.py                 # Defines tasks assigned to agents
│   └── utils/
│       ├── env_loader.py        # Loads environment variables
│       └── openai_client.py     # (Optional) LLM API handler
├── LICENSE
└── README.md
```


## 🚀 Features
->>🧾 PDF Data Extraction: Parses and extracts structured and unstructured text from uploaded bank statements.

- 🤖 Agent Roles:

- Financial Data Extraction Specialist: Extracts income, debit/credit, balances, etc.

- Risk Score Aggregator: Calculates financial ratios like DTI and Income Stability.

- Policy Compliance Officer: Checks for compliance issues (e.g., salary consistency, returns).

- Credit Decision Strategist: Makes the final creditworthiness decision based on all inputs.

- 📊 Structured Output: Produces detailed reasoning and justification for approval or denial.

- 🧩 Modular Design: Easily extensible for new agents, rules, or data formats.

## Installation Guide and .env file setup:
```
OPENAI_API_KEY=your-openai-api-key
MODEL=gpt-4  # or gpt-3.5-turbo or any local model if integrated
GOOGLE_API_KEY=your-google-api-key (optional if search tools used)

Clone:
git clone https://github.com/01kumarr/AI-Agent.git
cd AI-Agent

Create virtual env:
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```
### 🛠 Future Enhancements
- 🔍 Integrate OCR tools for scanned image PDFs.

- 🧠 Use LangChain/Ollama-compatible local models.

- 📡 Add API interface using FastAPI or Flask.

- 📈 Dashboard for reviewing agent outputs.
