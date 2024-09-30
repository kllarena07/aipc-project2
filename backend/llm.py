def generate_text(model, tokenizer, context, input_text):
    prompt = f"With help of the context: {context}\n\nAnswer the question: {input_text}"

    print(prompt)

    device = model.device
    inputs = tokenizer(prompt, return_tensors="pt", return_attention_mask=True)
    input_ids = inputs['input_ids'].to(device)
    attention_mask = inputs['attention_mask'].to(device)

    output = model.generate(input_ids, attention_mask=attention_mask, max_new_tokens=100)
    generated_sequence = output[0]
    new_tokens = generated_sequence[input_ids.shape[1]:]
    generated_text = tokenizer.decode(new_tokens, skip_special_tokens=True)

    return generated_text