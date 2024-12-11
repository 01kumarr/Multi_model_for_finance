LANGCHAIN_TRACING_V2="true"
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY="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"

from langsmith import evaluate, Client
from langsmith.schemas import Example, Run

# 1. Create and/or select your dataset
client = Client()
dataset_name = "my first dataset"
dataset = client.clone_public_dataset("https://smith.langchain.com/public/a63525f9-bdf2-4512-83e3-077dc9417f96/d", dataset_name=dataset_name)

# 2. Define an evaluator
def exact_match(outputs: dict, reference_outputs: dict) -> bool:
    return outputs == reference_outputs

# 3. Run an evaluation
# For more info on evaluators, see: https://docs.smith.langchain.com/concepts/evaluation#evaluators

# To evaluate an LCEL chain, replace lambda with chain.invoke
# To evaluate a LangGraph graph, replace lambda with graph.invoke
evaluate(
    lambda x: x["question"] + "is a good question. I don't know the answer.",
    # chain.invoke
    # graph.invoke
    data=dataset_name,
    evaluators=[exact_match],
    experiment_prefix="my first dataset experiment "
)