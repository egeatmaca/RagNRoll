from gpt4all import GPT4All
import multiprocessing


class GPT:
    def __init__(self, 
                 gpt='mistral-7b-openorca.gguf2.Q4_0.gguf',
                 n_threads=None):
        n_threads = n_threads if n_threads else multiprocessing.cpu_count()
        self.gpt = GPT4All(model_name=gpt, n_threads=n_threads)

    def generate(self, prompt: str):
        return self.gpt(prompt)