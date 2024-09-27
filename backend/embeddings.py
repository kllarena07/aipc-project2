from sentence_transformers import SentenceTransformer

def get_embeddings(docs, dimensions=512):
    model = SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1", truncate_dim=dimensions)
    embeddings = model.encode(docs)
    return embeddings
