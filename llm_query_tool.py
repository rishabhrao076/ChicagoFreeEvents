import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

# Hosted LLM

# API_URL = os.getenv("HF_INFERENCE_API_URL")
# headers = {"Authorization": "Bearer "+os.getenv("HF_BEARER_TOKEN")}

# def query(payload):
# 	payload = {"inputs": payload}
# 	print(payload)
# 	response = requests.post(API_URL, headers=headers, json=payload)
# 	return response.json()

# Local LLM

from langchain_community.llms import Ollama

def query(payload):
	llm = Ollama(model="mistral")
	response = llm.invoke(payload)
	return json.dumps(response)