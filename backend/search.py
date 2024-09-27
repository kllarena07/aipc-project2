from embeddings import get_embeddings

def vector_search(pc, index_name, namespace, dimensions, query, top_k=3):
    query_embedding = get_embeddings(query, dimensions).tolist()
    index = pc.Index(index_name)
    response = index.query(
        namespace=namespace,
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        include_values=True
    )

    return [
        {
            'id': match['id'],
            'score': match['score'],
            'metadata': match['metadata'],
            'value': match['values']
        }
        for match in response['matches']
    ]