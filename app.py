# app.py
import os
import json
import streamlit as st
from typing import List

# ─── llama-index imports ─────────────────────────────────────────────────────
from llama_index.core import VectorStoreIndex, Document
from llama_index.core.embeddings import BaseEmbedding
from llama_index.llms.together import TogetherLLM
from llama_index.core.settings import Settings

# ─── 3rd-party model import ───────────────────────────────────────────────────
from sentence_transformers import SentenceTransformer

# ─── CONFIG ───────────────────────────────────────────────────────────────────
# On Streamlit Cloud, set this in Settings → Secrets as:
# TOGETHER_API_KEY="sk-your-together-key"
TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]
os.environ["TOGETHER_API_KEY"] = TOGETHER_API_KEY

# ─── EMBEDDING ADAPTER ────────────────────────────────────────────────────────
class HFEmbedding(BaseEmbedding):
    """Wraps SentenceTransformer so llama-index can use it."""
    def __init__(self, model_name: str):
        super().__init__()
        self.model_name = model_name
        self._model     = None

    @property
    def model(self):
        if self._model is None:
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def _get_query_embedding(self, query: str) -> List[float]:
        return self.model.encode(query).tolist()

    def _get_text_embedding(self, text: str) -> List[float]:
        return self.model.encode(text).tolist()

    async def _aget_query_embedding(self, query: str) -> List[float]:
        # Async not needed in this example
        raise NotImplementedError

# ─── INDEX BUILDER (CACHED) ─────────────────────────────────────────────────
@st.cache_resource
def load_query_engine(json_path: str = "data/solefacts_tagged_data.json"):
    # 1) Load Reddit JSON
    with open(json_path, "r") as f:
        posts = json.load(f)

    # 2) Build Documents (text + metadata)
    docs = []
    for p in posts:
        chunks = [p.get("title",""), p.get("selftext","")] + p.get("comments", [])
        text   = "\n\n".join(chunks)
        # merge url + tags into metadata
        meta = {"url": p.get("url","<no-url>"), **p.get("tags", {})}
        docs.append(Document(text=text, metadata=meta))

    # 3) Init embedding + LLM
    embed_model = HFEmbedding("all-MiniLM-L6-v2")
    llm         = TogetherLLM(model="mistralai/Mistral-7B-Instruct-v0.2")

    # 4) Register in llama-index Settings
    Settings.embed_model = embed_model
    Settings.llm         = llm

    # 5) Build vector index + query engine
    index = VectorStoreIndex.from_documents(docs)
    return index.as_query_engine(similarity_top_k=5)

# Build once (cached)
query_engine = load_query_engine()

# ─── STREAMLIT UI ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="SoleFacts RAG App", layout="wide")
st.title("👟 SoleFacts: Ask Anything About Running Shoes")

user_query = st.text_input(
    "What do you want to know?", 
    placeholder="e.g. Which shoes are best for heel pain?"
)

if st.button("Get Answer") and user_query:
    with st.spinner("Searching community insights…"):
        response = query_engine.query(user_query)

    # 1) Show the generated answer
    st.markdown("### Answer")
    st.write(response.response)

    # 2) Show source URLs
    st.markdown("### Source Posts")
    for node in response.source_nodes:
        url = node.metadata.get("url", "#")
        st.markdown(f"- [{url}]({url})")
