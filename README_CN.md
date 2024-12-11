<div align="center">
<h1>
EasyDeploy
</h1>
</div>

<p align="center">
<div align="center">
<h4 align="center">
    <p>
        <b>中文</b> |
        <a href="">English</a>
    </p>
</h4>
</div>

## Contents
- [新闻](#新闻)
- [项目简介](#项目简介)
- [快速部署](#快速部署)
- [服务访问](#服务访问)
- [架构图](#架构图)
- [核心功能](#核心功能)
- [致谢](#致谢)
- [Contributing](#Contributing)

## 新闻
- [2024.11.06] EasyDeploy发布，基于docker+ollama的方式</font>

## 项目简介
EasyDeploy 旨在为用户提供端云一体的大模型部署能力，我们将大模型的部署和推理逻辑集成到 Docker 中，简化整体部署流程，全面提升用户体验。EasyDeploy 支持多种引擎，目前已支持 Ollama，未来将支持 vLLM 等其它引擎，进一步丰富用户的选择和应用场景。</font>

通过 EasyDeploy，用户能够快速在云端与端设备之间部署和启动大模型，消除技术壁垒，专注于模型本身的应用和优化。无论是在本地开发环境、云端平台还是端设备中，EasyDeploy 都将为用户提供高效、可靠的解决方案，助力人工智能的快速发展与应用落地。</font>

## 快速部署
### 环境依赖
+ python版本: 3.10
+ 依赖包安装：

```shell
pip install -r requirements.txt 
```
### 服务启动
Docker 镜像下载：

下载地址：上传后更新

```shell
docker run -p 8000:8000 easydeploy_llama3.2_3b 
```

## 服务访问
当前服务以restful API方式提供流批一体访问功能，请求demo 如下：

### chat页面
[http://127.0.0.1:8000/chat](http://127.0.0.1:8000/chat)

### API接口
#### 阻塞访问：
请求方式：

```python
# -*- coding: utf-8 -*-
import json
import requests
url = 'http://127.0.0.1:8000/chat/completions'
prompt = '你好'
model = 'lamma3.2'
messages = [{"role": "user", "content": prompt}]
data = {'model': model, 'messages': messages}
headers = {"Content-Type": "application/json"}
response = requests.post(url, headers=headers, data=json.dumps(data))
if response.status_code == 200:
    ans_dict = json.loads(response.text)
    print('data: {}'.format(ans_dict))
```

返回格式：

```json
{
    "id": "ollama-123",
    "object": "chat.completion",
    "created": 1731847899,
    "model": "lamma3.2",
    "system_fingerprint": "",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "你好,我是大语言模型，我主要的任务是提供帮助用户解决问题和解答问题，比如回答关于技术、编程、知识问答等。"
            },
            "logprobs": null,
            "finish_reason": "stop"
        }
    ],
    "usage": {

    }
}
```

### 流式访问：
请求方式：

```python
# -*- coding: utf-8 -*-
import json
import requests
url = 'http://127.0.0.1:8000/chat/completions'
prompt = '你好'
model = 'lamma3.2'
messages = [{"role": "user", "content": prompt}]
data = {'model': model, 'messages': messages, 'stream': True}
headers = {"Content-Type": "application/json"}
response = requests.post(url, headers=headers, data=json.dumps(data))
```

返回方式：

```json
{
  "id": "ollama-123",
  "object": "chat.completion.chunk",
  "created": 1731848401,
  "model": "lamma3.2",
  "system_fingerprint": "",
  "choices": [
    {
      "index": 0,
      "delta": {
        "role": "assistant",
        "content": "你"
      },
      "logprobs": null,
      "finish_reason": null
    }
  ]
}
```

### 架构图
![easydeploy modules](docs/easydeploy_modules_20241125.png)
### 核心能力
<table style="width: 100%; border: 1">
    <tr>
        <th style="width: 20%;">分类</th>
        <th style="width: 30%;">功能名称</th>
        <th style="width: 10%;">状态</th>
        <th style="width: 40%;">描述</th>
    </tr>
    <tr>
        <td rowspan="4">API Service</td>
        <td>基于Open AI的标准API规范</td>
        <td>✅</td>
        <td>服务接口遵循 OpenAI 规范，通过标准化 API 降低接入成本，用户可轻松集成功能，快速响应业务需求，专注于核心开发。</td>
    </tr>
    <tr>
        <td>阻塞式访问能力</td>
        <td>✅</td>
        <td>适用于需要完整性和准确性的任务，完成时结果进行整体校验或输出的任务，一次性获取完整输出。在整个过程中，用户需要等待直至所有输出内容完全完成。</td>
    </tr>
    <tr>
        <td>流式访问能力</td>
        <td>✅</td>
        <td>适用于对响应时间要求较高的实时应用，如代码补全、实时翻译或动态内容加载的场景。模型在生成过程中分段逐步传输内容，用户可在内容生成后立即接收和处理，无需等待全部完成，从而提升效率。</td>
    </tr>
    <tr>
        <td>高性能网络，提升用户开发能力</td>
        <td>⬜</td>
        <td>高性能网络通过优化数据传输、采用先进负载均衡算法及高效资源管理，能有效提升数据来源、降低延迟、提升响应速度。</td>
    </tr>
    <tr>
        <td rowspan="3">多引擎支持</td>
        <td>Ollama</td>
        <td>✅</td>
        <td>Ollama 以易用和轻量著称，专注于高效稳定的大模型推理服务。其友好 API 和简洁流畅流程，使开发者能够轻松将其手作快速部署应用。</td>
    </tr>
    <tr>
        <td>vLLM</td>
        <td>✅</td>
        <td>vLLM在内存管理和吞吐量上有显著优势，其通过优化存储和并行计算，显著提升推理速度和资源利用率，兼容多种硬件环境。vLLM提供丰富的配置选项，用户可根据需求调整推理策略，适用于实时和企业级应用。</td>
    </tr>
    <tr>
        <td>Tensorrt–LLM</td>
        <td>⬜</td>
        <td>TensorRT–LLM (TensorRT for Large Language Models) 是NVIDIA优化的高性能、大规模推理优化库，专为大型语言模型（LLM）设计。</td>
    </tr>
    <tr>
        <td>Docker部署能力</td>
        <td>基于python3.10构建Docker镜像</td>
        <td>✅</td>
        <td>将大型模型及其依赖的镜像，确保版本号一致运行，简化部署与配置。利用Docker的版本构建和自动化部署，提高模型更新与迭代效率，加快从开发到生产落地的转化。</td>
    </tr>
    <tr>
        <td>Web UI接入</td>
        <td>OpenUI 协议</td>
        <td>⬜</td>
        <td>丰富的UI开源协议便于用户整合多种组件，提升产品的定制性和扩展性。</td>
    </tr>
    <tr>
        <td>更多核心功能</td>
        <td>ModelCache语义缓存</td>
        <td>⬜</td>
        <td>通过缓存已有生成的QA Pair，使得请求变更更加细粒度，提高模型推理的性能与效率。</td>
    </tr>
</table>

## 致谢
本项目参考了以下开源项目，在此对相关项目和研究开发人员表示感谢。  
[Ollama](https://github.com/ollama/ollama)、[vLLM](https://github.com/vllm-project/vllm)

## Contributing
EasyDeploy是一个非常有趣且有用的项目，我们相信这个项目有很大的潜力，无论你是经验丰富的开发者，还是刚刚入门的新手，都欢迎你为这个项目做出一些贡献，包括但不限于：提交问题和建议，参与代码编写，完善文档和示例。

