import json
import faiss
import numpy as np
from flask import Flask, request, jsonify
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.schema import Document

app = Flask(__name__)

with open("courses_data.json", "r", encoding="utf-8") as file:
    courses = json.load(file)

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

texts = [course["title"] + " " + course.get("description", "") + " " + " ".join(course.get("details", [])) for course in courses]
metadata = [{"title": course["title"], "link": course.get("link", "N/A")} for course in courses]

embeddings = embedding_model.embed_documents(texts)

embeddings_np = np.array(embeddings, dtype=np.float32)

index = faiss.IndexFlatL2(embeddings_np.shape[1])
index.add(embeddings_np)

vector_store = FAISS(
    embedding_function=embedding_model,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={}
)

for i, doc in enumerate(texts):
    vector_store.docstore.add({str(i): Document(page_content=doc, metadata=metadata[i])})
    vector_store.index_to_docstore_id[i] = str(i) 
vector_store.save_local("faiss_index")

@app.route("/search", methods=["POST"])
def search():
    """API endpoint for searching courses."""
    data = request.get_json()
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400

    results = vector_store.similarity_search(query, k=1)

    if not results:
        return jsonify({"error": "No relevant courses found"}), 404

    best_match = results[0]

    print("Best match metadata:", best_match.metadata)

    return jsonify({
        "title": best_match.metadata.get("title", "No Title Found"),
        "link": best_match.metadata.get("link", "No Link Available"),
        "content": best_match.page_content
    })

if __name__ == "__main__":
    app.run(debug=True)
