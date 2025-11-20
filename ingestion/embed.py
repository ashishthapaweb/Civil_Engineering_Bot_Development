def create_embedddings(client, embedding_model, chunks):
    vectors = client.embeddings.create(
            model=embedding_model,
            input=chunks).data
    embeddings = [item.embedding for item in vectors]
    print(f"Embeddings created with total length: {len(embeddings)}")
    return embeddings