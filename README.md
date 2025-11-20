# Civil Engineering Bot Development

This is RAG (Retrieval-Augmented Generation)-based tool that turns a local PDF into embeddings with OpenAI, stores them in Chroma, and answers questions. There is a Streamlit UI (`app.py`) and the original script (`main.py`).

## How it works
- `ingestion/extract.py` pulls text from `knowledgebase/CV_Thapa.pdf`, cleans it, and caches a `.md` next to the PDF.
- `ingestion/chunk.py` tokenizes and chunks the markdown; the first empty chunk is dropped in `rag/run.py`.
- `ingestion/embed.py` builds embeddings; `vectorstore/chroma_store.py` persists them to `./chroma`.
- `rag/run.py` wires retrieval + prompting + LLM call via OpenAI; `answer_query()` is what the UI uses.
- `app.py` is a tiny Streamlit front end to ask questions; `main.py` is a CLI example (uses the hard-coded `USER_QUERY`).

## Setup
- Python 3.12+ recommended. Create/activate a venv.
- Install deps: `pip install -r requirements.txt`.
- Add your key in `.env` (`OPENAI_API_KEY=...`; see `.env.example`).

## Run
- Streamlit UI: `streamlit run app.py`
- CLI example: `python main.py` (edit `USER_QUERY` in `main.py`).
- If you replace the source PDF, change the path in `extract_and_clean_pdf` and delete the cached `.md` so it re-extracts.
