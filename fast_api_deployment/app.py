import torch
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from uvicorn.workers import UvicornWorker

from transformers import GPTNeoXForCausalLM, AutoTokenizer

model = GPTNeoXForCausalLM.from_pretrained(
  "EleutherAI/pythia-70m-deduped",
  revision="step3000",
)

tokenizer = AutoTokenizer.from_pretrained(
  "EleutherAI/pythia-70m-deduped",
  revision="step3000",
)

app = FastAPI()

class ParameterInput(BaseModel):
    max_new_tokens: int = 50
    repetition_penalty: float = 1.03
    temperature: float = 0.5
    top_k: int = 10
    top_p: float = 0.95


class InputPrompt(BaseModel):
    input: str = "My name is Olivier and I"
    parameters: ParameterInput


class GeneratedText(BaseModel):
    text: str


@app.post("/generate", response_model=GeneratedText)
async def generate_func(data: InputPrompt):
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=data.parameters.max_new_tokens,
        do_sample=True,
        temperature=data.parameters.temperature,
        top_p=data.parameters.top_p,
        top_k=data.parameters.top_k,
        repetition_penalty=data.parameters.repetition_penalty,
    )
    prompt_template = f"{data.input}"
    output = pipe(prompt_template)
    return {"text": output[0]["generated_text"]}
