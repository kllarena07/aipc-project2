from optimum.intel import OVModelForCausalLM
from transformers import AutoTokenizer
from openvino.runtime import Core

# Initialize OpenVINO Core
core = Core()
core.set_property({"CACHE_DIR": "./model_cache"})

# Load the model
model_id = "Gunulhona/openvino-llama-3.1-8B_int8"
model = OVModelForCausalLM.from_pretrained(
    model_id,
    device="GPU",
    ov_config={"CACHE_DIR": "./model_cache"}
)

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_id)

# Set pad token
tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = tokenizer.pad_token_id

# Prepare input text
input_text = "Hello, how are you today?"

# Tokenize input with attention mask
inputs = tokenizer(input_text, return_tensors="pt", return_attention_mask=True)
input_ids = inputs['input_ids']
attention_mask = inputs['attention_mask']

# Generate text
output = model.generate(input_ids, attention_mask=attention_mask, max_length=50)

# Decode the output
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

print(generated_text)