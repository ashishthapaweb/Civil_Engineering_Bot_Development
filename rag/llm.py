def ask_llm(client, gpt_model, messages):
    llm_response = client.chat.completions.create(
        messages=messages,
        model = gpt_model,
        temperature=0
    )
    
    llm_output = llm_response.choices[0].message.content
    return llm_output