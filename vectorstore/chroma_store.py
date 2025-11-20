import chromadb

# Initialize the chroma client with a persistent directory
chroma = chromadb.PersistentClient(path="./chroma")

def create_collection(embeddings, chunks):
    collection = chroma.get_or_create_collection(
        name="my_code",
        metadata={"hnsw:space": "cosine"}
    )

    ids = [f"chunk-{i}" for i in range(len(chunks))]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=[{"source":"IS4562000.pdf"} for _ in chunks]
    )
    
    return collection