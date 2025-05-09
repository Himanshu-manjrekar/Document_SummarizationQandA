# Code to store data in vector DB FAISS
# For now we are using FAISS Index in Future Enhancement we will Implement Chrom or pineconedb
import faiss

class creat_vector_db():
    def __init__(self):
        pass

    def create_faiss_index(self, encodded_data):
        # chunks_embeddings_dimension :- 384 
        chunks_embeddings_dimension = encodded_data.shape[1]
        # create Faiss index (L2 Distance)
        index = faiss.IndexFlatL2(chunks_embeddings_dimension)
        index.add(encodded_data)
        return index