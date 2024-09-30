def generate_text(model, tokenizer, context, input_text):
    prompt = f"""
        You are an LLM that specializes in answering questions with accurate information.
        If you do not know the answer. Answer with "I do not know."
        Using the context providede below, generate a response to the following question:

        Context:
        ========================
        {context}
        ========================

        Question: {input_text}
    """

    # print(prompt)

    inputs = tokenizer(prompt, return_tensors="pt", return_attention_mask=True)
    input_ids = inputs['input_ids']
    attention_mask = inputs['attention_mask']

    output = model.generate(input_ids, attention_mask=attention_mask, max_new_tokens=100)
    # print(output)

    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    # print(generated_text)

    return generated_text
