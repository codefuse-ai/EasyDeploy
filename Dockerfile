FROM python:3.10

ADD . /workspace/code-repo
WORKDIR /workspace/code-repo

RUN pip install fastapi uvicorn
RUN pip3 install requests

ENV PYTHONPATH /workspace/code-repo

RUN apt-get update && apt-get install -y curl

RUN curl -fsSL https://ollama.com/install.sh | sh

RUN ollama serve
RUN ollama run llama3.2

ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 8000

CMD sh -c "ollama serve & ollama run llama3.2"
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--load-balancer", "sunrpc"]
