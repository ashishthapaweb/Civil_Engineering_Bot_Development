import os
from openai import OpenAI
from dotenv import load_dotenv; load_dotenv(".env", override=True)
# Local imports
from ingestion.extract import extract_and_clean_pdf
from ingestion.chunk import chunk_markdown
from ingestion.embed import create_embedddings
from vectorstore.chroma_store import create_collection
from rag.retrieval import retrieve_info
from rag.prompt import generate_prompt
from rag.llm import ask_llm
 
# OpenAI Models
GPT_MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "<Type Here>"))

# EXTRACTING AND CLEANING TEXT
md_clean = extract_and_clean_pdf(r".\knowledgebase\CV_Thapa.pdf")

# CHUNKING THE MARKDOWN
# First chunk is empty string so starting from 1
chunks = chunk_markdown(md_clean)[1:]

# CREATE EMBEDDINGS
embeddings = create_embedddings(client, EMBEDDING_MODEL, chunks)

# STORE EMBEDDINGS IN VECTOR DATABASE
collection = create_collection(embeddings, chunks)

# PERFORM RAG OPERATION
USER_QUERY = "What am I doing with Prof. Huan Zhang?"
retrieved_data = retrieve_info(client, EMBEDDING_MODEL, USER_QUERY, collection)
messages = generate_prompt(USER_QUERY, retrieved_data)
llm_response = ask_llm(client, GPT_MODEL, messages)

print(llm_response)