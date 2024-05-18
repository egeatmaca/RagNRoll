from transformers import pipeline


class Summarizer:
    pipe = pipeline('summarization', model='cnicu/t5-small-booksum')

    def summarize(self, texts: list[str]):
        return [x['summary_text'] for x in self.pipe(texts)]