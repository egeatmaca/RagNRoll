import nltk


class Chunker:
    def chunk(self, documents: str, chunk_size: int = 512):
        chunks = []
        for document in documents:
            sentences = nltk.sent_tokenize(document)
            chunk = ''
            for sentence in sentences:
                chunk_prev = chunk
                chunk = chunk + ' ' + sentence
                if nltk.word_tokenize(chunk) > chunk_size:
                    chunks.append(chunk_prev)
                    chunk = sentence
            if chunk != '':
                chunks.append(chunk)
        return chunks