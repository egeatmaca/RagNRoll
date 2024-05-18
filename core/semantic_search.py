import os
import uuid
import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import time
from core.chunker import Chunker


class SemanticSearch:
    def __init__(self, 
                 model_name: str = 'all-MiniLM-L6-v2',
                 similarity: str = 'cosine',
                 host: str = None, 
                 port: int = None, 
                 collection: str = 'documents'):
        
        self.embedding_function = SentenceTransformerEmbeddingFunction(model_name)
        
        host = host if host else os.environ.get('CHROMADB_HOST')
        port = port if port else os.environ.get('CHROMADB_PORT')
        settings = Settings(allow_reset=True, anonymized_telemetry=False)
        
        if host and port:
            client = chromadb.HttpClient(host=host, port=port, settings=settings)
        else:
            client = chromadb.Client()

        while True:
            try:
                self.collection = client.get_or_create_collection(name=collection, metadata={"hnsw:space": similarity})
                break
            except Exception as e:
                print(e)
                time.sleep(5)
                continue

    def add(self, documents: list[str], metadatas: list[str] = None):
        chunker = Chunker()
        chunks = chunker.chunk(documents)
        embeddings = self.embedding_function(chunks)
        ids = [str(uuid.uuid4()) for _ in range(len(chunks))]
        metadatas = [None] * len(chunks) if not metadatas else metadatas
        print('LEN:', len(chunks), len(embeddings), len(ids), len(metadatas))
        self.collection.add(documents=chunks, ids=ids, embeddings=embeddings, metadatas=metadatas)

    def query(self, query_text: str, n_results: int = 1):
        query_embeddings = self.embedding_function([query_text])
        return self.collection.query(query_embeddings=query_embeddings, n_results=n_results)

    def inject_documents(self, documents_dir='documents'):
        for doc_name in os.listdir(documents_dir):
            doc_path = os.path.join(documents_dir, doc_name)
            doc_id = doc_name.replace('.txt', '').strip()
            with open(doc_path, 'r', encoding='utf-8', errors='ignore') as doc:
                document = doc.read()
                self.add(documents=[document])
            print(f'Document {doc_id} injected!')