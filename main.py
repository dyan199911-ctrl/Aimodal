import os
from fastapi import FastAPI
from pydantic import BaseModel
from vllm import LLMEngine, EngineArgs, SamplingParams
import uuid

app = FastAPI(title="Qwen 32B Dedicated Private API")

# إعداد المحرك الخاص بك والمحسن تماماً لمنع أي تعليق في بيئة Render
MODEL_NAME = "Qwen/Qwen2.5-32B-Instruct-AWQ"

engine_args = EngineArgs(
    model=MODEL_NAME,
    quantization="awq",
    max_model_len=2048,
    gpu_memory_utilization=0.85, # استغلال مثالي لذاكرة الكرت الخاصة بسيرفرك
    enforce_eager=True
)

# تشغيل المحرك فور إقلاع السيرفر ليبقى ساخناً دائماً
engine = LLMEngine.from_engine_args(engine_args)

class QueryRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate(request: QueryRequest):
    sampling_params = SamplingParams(temperature=0.7, top_p=0.9, max_tokens=512)
    request_id = str(uuid.uuid4())
    
    engine.add_request(request_id, request.prompt, sampling_params)
    
    output_text = ""
    while engine.has_unfinished_requests():
        request_outputs = engine.step()
        for request_output in request_outputs:
            if request_output.request_id == request_id:
                output_text = request_output.outputs[0].text
                
    return {"response": output_text}

@app.get("/health")
def health_check():
    return {"status": "healthy", "model": "Qwen-32B-Private"}
