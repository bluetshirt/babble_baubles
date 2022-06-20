import requests
import json 
import logging
import os 


logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
                    
class GPTException(Exception):
    pass

class GPT:
    
    def __init__(self, engine_id = "gptj_6B", top_p = 0.9, top_k = 40, max_tokens = 400, temperature = 1.0):
        self.engine_id = engine_id
        self.top_p = top_p
        self.top_k = top_k
        self.max_tokens = max_tokens
        self.temperature = temperature
        
    def predict(self, prompt):
        return gpt(prompt, self.engine_id, self.top_p, self.top_k, self.max_tokens, self.temperature)

    def __str__(self):
        message = f"""Settings:
Engine: {self.engine_id} 
top_p: {self.top_p} 
top_k: {self.top_k} 
max_tokens: {self.max_tokens} 
temperature: {self.temperature} 
"""
        return message

def gpt(prompt, engine_id = "gptj_6B", top_p = 0.9, top_k = 40, max_tokens = 400, temperature = 1.0):

    url = f"https://api.textsynth.com/v1/engines/{engine_id}/completions"
    
    req_body = {'prompt': prompt, 'top_p': top_p, 'top_k': top_k, 'max_tokens': max_tokens, "temperature": temperature}
    
    api_key = os.environ.get("TEXTSYNTH_KEY")
    
    req_headers = {
      "Content-Type": "application/json" ,
      "Authorization" : f"Bearer {api_key}"
    }

    x = requests.post(url, data = json.dumps(req_body), headers = req_headers)
    
    logger.info(url)
    logger.info(req_body)
    logger.info(json.loads(x.text))
    
    result = json.loads(x.text)

    try:
        completion = result["text"]
    except KeyError as k:
        raise GPTException(result["error"])
    
    return completion
