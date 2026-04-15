import os
import json
import ollama
from dotenv import load_dotenv
import pageindex.utils as utils

load_dotenv()
CHAT_LLM_NAME = os.getenv("CHAT_LLM_NAME")

OLLAMA_URL = os.getenv("OLLAMA_URL")
client = ollama.AsyncClient(host=OLLAMA_URL)

# +
async def call_llm_json(prompt, model=CHAT_LLM_NAME, temperature=0):

    response = await client.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        format="json", 
        options={
            "temperature": temperature
        } 
    )
    return response['message']['content'].strip()

async def call_llm(prompt, model=CHAT_LLM_NAME, temperature=0):

    response = await client.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        options={
            "temperature": temperature
        }
    )
    return response['message']['content'].strip()
# -

# You can also use our GitHub repo to generate PageIndex tree
# https://github.com/VectifyAI/PageIndex

with open("./results/The-AI-Act_structure.json", "r") as jsonfile: 
    data = json.load(jsonfile)
tree = data["structure"]

#query = "What are the conclusions in this document?"
query = "What are the different AI risk levels defined in this document?"

tree_without_text = utils.remove_fields(tree.copy(), fields=['text'])

search_prompt = f"""
You are given a question and a tree structure of a document.
Each node contains a node id, node title, and a corresponding summary.
Your task is to find all nodes that are likely to contain the answer to the question.

Question: {query}

Document tree structure:
{json.dumps(tree_without_text, indent=2)}

Please reply in the following JSON format:
{{
    "thinking": "<Your thinking process on which nodes are relevant to the question>",
    "node_list": ["node_id_1", "node_id_2", ..., "node_id_n"]
}}
Directly return the final JSON structure. Do not output anything else.
"""

tree_search_result = await call_llm_json(search_prompt)

node_map = utils.create_node_mapping(tree)
tree_search_result_json = json.loads(tree_search_result)

print('Reasoning Process:')
utils.print_wrapped(tree_search_result_json['thinking'])

print('\nRetrieved Nodes:')
for node_id in tree_search_result_json["node_list"]:
    node = node_map[node_id]
    print(f"Node ID: {node['node_id']}\t Start index: {node['start_index']}\t Title: {node['title']}")

node_list = tree_search_result_json["node_list"]
relevant_content = "\n\n".join(node_map[node_id]["text"] for node_id in node_list)

print('Retrieved Context:\n')
utils.print_wrapped(relevant_content[:1000] + '...')

answer_prompt = f"""
Answer the question based on the context:

Question: {query}
Context: {relevant_content}

Provide a clear, concise answer based only on the context provided.
"""

print('Generated Answer:\n')
answer = await call_llm(answer_prompt)
utils.print_wrapped(answer)
