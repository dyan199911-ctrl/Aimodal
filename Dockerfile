FROM nvidia/cuda:12.1.1-devel-ubuntu22.04

RUN apt-get update && apt-get install -y python3-pip python3-dev && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir vllm==0.4.0.post1 torch==2.1.2 fastapi uvicorn pydantic

WORKDIR /app
COPY main.py /app/main.py

EXPOSE 10000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
