# -*- coding: utf-8 -*-
import requests
import json

url_generate = "http://127.0.0.1:11434/api/generate"


def get_response(url, data):
    response = requests.post(url, json=data)
    response_dict = json.loads(response.text)
    response_content = response_dict["response"]
    return response_content


data = {
    "model": "llama3.2",
    "prompt": "hello",
    "stream": False
}

res = get_response(url_generate,data)
print(res)
