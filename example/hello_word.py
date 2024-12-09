# -*- coding: utf-8 -*-
import json
import requests


def run():
    url = 'http://127.0.0.1:5000/'
    headers = {"Content-Type": "application/json"}
    res = requests.post(url, headers=headers)
    res_text = res.text
    print('res_text: {}'.format(res_text))


if __name__ == '__main__':
    run()
