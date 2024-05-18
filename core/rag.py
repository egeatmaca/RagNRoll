from gpt4all import GPT4All
import multiprocessing
from core.semantic_search import SemanticSearch


class RAG:
    def __init__(self, 
                 gpt='mistral-7b-openorca.gguf2.Q4_0.gguf', 
                 gpt_threads=None,
                 sentence_transformer='all-MiniLM-L6-v2', 
                 similarity='cosine',
                 chromadb_host=None, 
                 chromadb_port=None, 
                 chromadb_collection='documents'):
        self.gpt_threads = gpt_threads if gpt_threads else multiprocessing.cpu_count()
        self.gpt = GPT4All(model_name=gpt, n_threads=self.gpt_threads)
        self.semantic_search = SemanticSearch(
            model_name=sentence_transformer, 
            similarity=similarity, 
            host=chromadb_host, 
            port=chromadb_port, 
            collection=chromadb_collection
        )

    def retrieve_documents(self, prompt, n_results=1):
        search_results = self.semantic_search.query(prompt, n_results)
        print('Search Results:', search_results)
        documents = search_results['documents'][0]
        return documents

    def augment_prompt(self, prompt, documents):
        context = 'Use the following information in your answer:\n' 
        context += '\n'.join(documents)
        prompt = context + '\n\n' + prompt
        return prompt

    def generate(self, prompt, n_results=1):
        documents = self.retrieve_documents(prompt, n_results)
        prompt = self.augment_prompt(prompt, documents)
        generated_text = self.gpt.generate(prompt, n_batch=self.gpt_threads)
        print('Generated Text:', generated_text)
        return generated_text
