import nltk
nltk.download('punkt')


class Chunker:
    # def chunk(self, documents: list[str], chunk_size: int = 216):
    #     chunks = []
    #     for document in documents:
    #         sentences = nltk.sent_tokenize(document)
    #         chunk = ''
    #         for sentence in sentences:
    #             chunk_prev = chunk
    #             chunk += ' ' + sentence
    #             if len(nltk.word_tokenize(chunk)) > chunk_size:
    #                 chunks.append(chunk_prev)
    #                 chunk = sentence
    #         if chunk != '':
    #             chunks.append(chunk)
    #     return chunks

    def chunk(self, documents: list[str], chunk_size: int = 216):
        chunks = []
        for document in documents:
            tokens = nltk.word_tokenize(document)
            n_tokens = len(tokens)
            n_chunks = n_tokens // chunk_size + 1
            for i in range(n_chunks):
                j = min((i + 1) * chunk_size, n_tokens)
                if i > j: break
                chunk = ' '.join(tokens[i:j])
                chunks.append(chunk)
        print('CHUNKS:', chunks)
        return chunks