def generate_prompt(user_query, retrieved_data):
    prompt = "Based on this retrieved message from the knowledgebase, answer user's question.\n"
    prompt += f"Retrieved Message: {retrieved_data}\n"
    prompt += f"User's question: {user_query}\n"
    prompt += "Provide direct answers in 1-2 sentences."
    
    messages = [
    {'role':'system', 'content': 'You answer questions provided by the user in a direct manner.'},
    {'role':'user', 'content': prompt}]
    
    
    return messages
