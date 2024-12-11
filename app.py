# -*- coding: utf-8 -*-
import requests
from fastapi.responses import StreamingResponse
import time
import json
from typing import Iterator
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


app = FastAPI()
templates = Jinja2Templates(directory="templates")  # Specify the template directory here.
url_generate = "http://127.0.0.1:11434/api/generate"  # Ollama API 地址


class UserInput(BaseModel):
    prompt: str
    stream: bool = False  # Optional field


class UserOutput(BaseModel):
    model_reply: str


def get_response(model: str, prompt: str) -> str:
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False  # 暂时不处理流式输出
    }
    try:
        response = requests.post(url_generate, json=data)
        response.raise_for_status()
        response_dict = response.json()
        return response_dict.get("response", "没有收到响应。")
    except requests.exceptions.RequestException as e:
        return f"请求 Ollama 服务时出错: {e}"


@app.get("/hello_word", response_class=HTMLResponse)
async def home():
    return 'Hello Word！'


@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("chat_page.html", {"request": request})


@app.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()
        user_input = body.get("user_input")
        model = body.get("model")

        if not user_input or not model:
            return JSONResponse(status_code=400, content={"reply": "缺少 user_input 或 model 参数。"})

        reply = get_response(model, user_input)
        return {"reply": reply}

    except Exception as e:
        return JSONResponse(status_code=500, content={"reply": f"内部服务器错误: {e}"})


# @app.post("/generate")
@app.post("/chat/completions")
async def generate(request: Request):
    # 从请求中解析 JSON 数据
    request_dict = await request.json()
    model = request_dict.get("model", "")
    messages = request_dict.get("messages", dict())
    stream = request_dict.get("stream", False)
    prompt = messages[-1].get("content", "")

    data = {
        "model": model,
        "prompt": prompt,
        "stream": stream
    }
    # url_generate = "http://127.0.0.1:11434/api/generate"

    if stream:
        # 如果需要流式响应
        promise = requests.post(url_generate, json=data, stream=True)

        def number_stream() -> Iterator[str]:
            for number in promise.iter_lines():
                number_dict = json.loads(number.decode('utf-8'))
                model_reply = number_dict['response']
                result = {
                    "id": "ollama-123",
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": model,
                    "system_fingerprint": "",
                    "choices": [
                        {
                            "index": 0,
                            "delta": {
                                "role": "assistant",
                                "content": model_reply
                            },
                            "logprobs": None,
                            "finish_reason": None
                        }
                    ]
                }
                # yield f"{number.decode('utf-8')}\n"
                yield f"{json.dumps(result)}\n"

        return StreamingResponse(number_stream())
    else:
        # 如果不需要流式响应
        print('非流式分支...')
        response = requests.post(url_generate, json=data)
        if response.status_code == 200:
            response_dict = json.loads(response.text)
            response_content = response_dict["response"]
            model_reply = response_content
            finish_reason = "stop"
        else:
            model_reply = "与模型通信失败。"
            finish_reason = "error"

        result = {
            "id": "ollama-123",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model,
            "system_fingerprint": "",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": model_reply,
                },
                "logprobs": None,
                "finish_reason": finish_reason
            }],
            "usage": {}
            }
        return JSONResponse(result)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
