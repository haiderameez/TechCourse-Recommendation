import json
import faiss
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.schema import Document

# Load JSON data
with open("courses_data.json", "r", encoding="utf-8") as file:
    courses = json.load(file)

# Initialize Hugging Face Embeddings
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Prepare data for embeddings
texts = [course["title"] + " " + course["description"] + " " + " ".join(course["details"]) for course in courses]
metadata = [{"title": course["title"]} for course in courses]  # Removed 'link' from metadata

# Generate embeddings
embeddings = embedding_model.embed_documents(texts)

# Convert embeddings to NumPy array
embeddings_np = np.array(embeddings, dtype=np.float32)

# Create FAISS index
index = faiss.IndexFlatL2(embeddings_np.shape[1])  # L2 Distance
index.add(embeddings_np)

# Store data in FAISS
vector_store = FAISS(
    embedding_function=embedding_model,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={}
)

for i, doc in enumerate(texts):
    vector_store.docstore.add({str(i): Document(page_content=doc, metadata=metadata[i])})  # Fixed `.add()`

# Save FAISS index
vector_store.save_local("faiss_index")
