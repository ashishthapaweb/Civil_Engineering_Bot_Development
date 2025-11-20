# RAG Playground

Small RAG script that turns a local PDF into embeddings with OpenAI, stores them in a Chroma DB folder, and answers a hard‑coded question.

## What it does
- `ingestion/extract.py` pulls text from `knowledgebase/CV_Thapa.pdf`, cleans it, and saves a `.md` next to the PDF.
- `ingestion/chunk.py` tokenizes and chunks the markdown; the first empty chunk is skipped in `main.py`.
- `ingestion/embed.py` creates embeddings with OpenAI; `vectorstore/chroma_store.py` persists them in `./chroma`.
- `rag/retrieval.py` finds the top match for the query; `rag/prompt.py` frames the reply; `rag/llm.py` calls the chat model.

## Setup
- Python 3.12+ recommended. Create/activate a venv.
- Install deps: `pip install -r requirements.txt`.
- Put your key in `.env` (`OPENAI_API_KEY=...`; see `.env.example`).

## Run
- `python main.py`
- Change `USER_QUERY` in `main.py` if you want a different question.
- If you swap the source PDF, set the new path in `extract_and_clean_pdf` and delete the old `.md` so it re-extracts.
