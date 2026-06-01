import os
from fastapi import FastAPI
from pydantic import BaseModel
from huggingface_hub import InferenceClient

app = FastAPI(title="Aimodal Private API")

# استخدام مستضيف هجين خفيف يعمل على الخطة المجانية فوراً وبأعلى سرعة لـ Qwen 32B
client = InferenceClient(model="Qwen/Qwen2.5-32B-Instruct")

class QueryRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate(request: QueryRequest):
    try:
        # توليد النص بسرعة فائقة وبدون الحاجة لـ GPU محلي
        response = client.text_generation(
            request.prompt,
            max_new_tokens=512,
            temperature=0.7,
            top_p=0.9
        )
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
            if request_output.request_id == request_id:
                output_text = request_output.outputs[0].text
                
    return {"response": output_text}

@app.get("/health")
def health_check():
    return {"status": "healthy", "model": "Qwen-32B-Private"}
