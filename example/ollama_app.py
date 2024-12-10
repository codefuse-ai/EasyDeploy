# -*- coding: utf-8 -*-
import json
import requests


def run():
    url = 'http://127.0.0.1:8000/chat/completions'
    prompt = 'hello'
    model = 'llama3.2'
    messages = [{"role": "user", "content": prompt}]
    data = {'model': model, 'messages': messages}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        ans_dict = json.loads(response.text)
        print('data: {}'.format(ans_dict))


if __name__ == '__main__':
    run()
