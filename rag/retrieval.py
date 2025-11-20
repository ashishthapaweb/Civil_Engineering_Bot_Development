def retrieve_info(client, model, query, collection):
    query_vec = client.embeddings.create(
        model=model,
        input=query
    ).data[0].embedding

    result = collection.query(
        query_embeddings=[query_vec],
        n_results=5
    )

    retrieved_data = result['documents'][0][0]
    return retrieved_data