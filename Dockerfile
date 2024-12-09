#FROM python:3.8-slim-buster
FROM python:3.10

# 将当前目录的所有内容复制到目标目录
ADD . /workspace/code-repo
# 设定后续操作的工作目录为 /workspace/code-repo，有利于提升可读性和管理效率
WORKDIR /workspace/code-repo

RUN pip install fastapi uvicorn
RUN pip3 install requests

ENV PYTHONPATH /workspace/code-repo

# 安装依赖工具，例如 curl 和 sh（如果尚未安装）
RUN apt-get update && apt-get install -y curl

# 执行 Ollama 安装脚本
RUN curl -fsSL https://ollama.com/install.sh | sh

# 安装完成后，启动ollama服务
#RUN ollama serve
#RUN ollama run qwen2:0.5b

# 设置环境变量以允许 Flask 绑定到所有可用的 IP
ENV FLASK_RUN_HOST=0.0.0.0

# 暴露 Flask 默认端口
EXPOSE 8000

# ENTRYPOINT [ "python3", "./app_stream.py" ]
# CMD ["flask", "run"]

CMD sh -c "ollama serve & ollama run llama3.2"
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--load-balancer", "sunrpc"]
