from sentence_transformers import SentenceTransformer

model_name = "mixedbread-ai/mxbai-embed-large-v1"

def get_embeddings(docs, dimensions=512):
    model = SentenceTransformer(model_name, truncate_dim=dimensions)
    embeddings = model.encode(docs)
    return embeddings
