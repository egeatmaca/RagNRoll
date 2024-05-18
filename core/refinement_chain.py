import nltk
from .gpt import GPT


class RefinementChain:
    gpt = GPT()
    prompt_template = 'Context: {context}\n\nInstruction: {instruction}\n\nText: {text}\n\nRefine the text following the instructions and using the context.'
    
    def refine(self, intruction: str, text: str, context: list[str], max_tokens: int=500):
        refined_text = text
        for chunk in context:
            prompt = self.prompt_template.format(context=chunk, instruction=intruction, text=refined_text)
            refined_text = self.gpt.generate(prompt, max_tokens=max_tokens)