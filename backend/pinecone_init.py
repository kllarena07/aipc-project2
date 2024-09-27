from pinecone import Pinecone, ServerlessSpec

def create_pinecone(api_key, index_name, dimensions=512):
    pc = Pinecone(api_key=api_key)
    dimensions = dimensions

    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            dimension=dimensions,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
    
    return pc