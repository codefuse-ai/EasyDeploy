# -*- coding: utf-8 -*-
import json
import requests


# 发起请求，并将stream参数设置为True以获取流式输出
url = 'http://127.0.0.1:8000/chat/completions'
prompt = '你是谁？'
model = 'qwen2:0.5b'
messages = [{"role": "user", "content": prompt}]
data = {'model': model, 'messages': messages, 'stream': True}
headers = {"Content-Type": "application/json"}

response = requests.post(url, headers=headers, data=json.dumps(data))

resp = ''
for line in response.iter_lines():
    print('line: {}'.format(line))
    print('line: {}'.format(type(line)))
    data = line.decode('utf-8')
    print('data: {}'.format(data))
    print('data: {}'.format(type(data)))
    data_dict = json.loads(data)
    print('data_dict: {}'.format(data_dict))
    print('data_dict: {}'.format(type(data_dict)))
    text = data_dict['choices'][-1]['delta']['content']
    resp += text
print('resp: {}'.format(resp))
