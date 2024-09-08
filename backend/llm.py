import openvino_genai as ov_genai

model_path = "TinyLlama"
pipe = ov_genai.LLMPipeline(model_path, "GPU")

prompt = "The Sun is yellow because"
response = pipe.generate(prompt, max_new_tokens=100)
print(response)
