from pageindex import PageIndexClient
import pageindex.utils as utils

import os
from dotenv import load_dotenv
load_dotenv()

# Get your PageIndex API key from https://dash.pageindex.ai/api-keys
PAGEINDEX_API_KEY = os.getenv("PAGEINDEX_API_KEY")
pi_client = PageIndexClient(api_key=PAGEINDEX_API_KEY)

import openai
OPENAI_API_KEY = os.getenv("CHATGPT_API_KEY")

async def call_llm(prompt, model="gpt-4.1", temperature=0):
    client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)
    response = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    return response.choices[0].message.content.strip()

    import os, requests

# You can also use our GitHub repo to generate PageIndex tree
# https://github.com/VectifyAI/PageIndex

import os
pdf_url = "https://artificialintelligenceact.eu/wp-content/uploads/2021/08/The-AI-Act.pdf"
pdf_path = os.path.join("./data", pdf_url.split('/')[-1])
os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

import requests
response = requests.get(pdf_url)
with open(pdf_path, "wb") as f:
    f.write(response.content)
print(f"Downloaded {pdf_url}")

# doc_id = pi_client.submit_document(pdf_path)["doc_id"]
doc_id = "pi-cmmj17gz40821ksqn34ymbh2e"
print('Document Submitted:', doc_id)

if pi_client.is_retrieval_ready(doc_id):
    tree = pi_client.get_tree(doc_id, node_summary=True)['result']
    print('Simplified Tree Structure of the Document:')
    utils.print_tree(tree)
else:
    print("Processing document, please try again later...")

import json

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

tree_search_result = await call_llm(search_prompt)

node_map = utils.create_node_mapping(tree)
tree_search_result_json = json.loads(tree_search_result)

print('Reasoning Process:')
utils.print_wrapped(tree_search_result_json['thinking'])

print('\nRetrieved Nodes:')
for node_id in tree_search_result_json["node_list"]:
    node = node_map[node_id]
    print(f"Node ID: {node['node_id']}\t Page: {node['page_index']}\t Title: {node['title']}")

node_list = json.loads(tree_search_result)["node_list"]
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
