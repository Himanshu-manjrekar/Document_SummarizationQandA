# the code for Initializing the GGUf model and Inferencing the prompt.

# general work flow
    # 1. Initialization of model
    # 2. As we have have based Q and A we need similar chunks w.r.t user question
    #   2a. Similar chunks using similarity search
    #       2aa. Encode the Data i.e out text from the documents
    #       2ab. Create Vector Store of this encoded_data ans store it (FAISS) 
    #       2ac. Perform similarity search between user query(Question) and vectors from vector Store and return similar chunks
    #   2b. Append this similar chunks with our prompt 
    # 3. Pass prompt to generate Inference

import os
import re
import numpy as np
import streamlit as st

from dataclasses import dataclass
from llama_cpp import Llama 
# from .vector_db import creat_vector_db
from .vector_db import creat_vector_db
from sentence_transformers import SentenceTransformer
from pathlib import Path


@dataclass
class chat_model_config:
    gguf_model_path: str = os.path.join("src\\components\\artifacts\\models\\tiny_llama", "tinyllama.gguf")
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"

class chat_model:
    def __init__(self):
        self.configs = chat_model_config()

    # 1. Initialization of Model
    def init_model(self):
        try:
            tiny_llama = Llama(model_path=str(self.configs.gguf_model_path))
            print("✅ Tiny_llama initialized successfully")
            return tiny_llama

        except Exception as e:
            print("🚨 Error while initializing model:")
            print(e)

    # 2aa. Encode the data 
    def encode_data(self, data):
        embedding_model = SentenceTransformer(self.configs.embedding_model_name)
        embedded_data = embedding_model.encode(data).astype(np.float32)
        return embedded_data

    # 2ab. create Vector Store of the encoded_data and store it
    def create_store_vector(self, data):
        # we will create index of encodded data for search
        v_db = creat_vector_db()
        encoded_index = v_db.create_faiss_index(data)
        return encoded_index
        
    # 2ac. Perform similarity Search between encodded data and user query
    def similarity_results(self, data, user_query, chunks):
        top_k = 3
        encoded_user_query =  self.encode_data(user_query).reshape(1, -1)
        indices = self.create_store_vector(data)

        similar_indexes = indices.search(encoded_user_query, top_k)[1]
        similarity_results = [chunks[result] for result in similar_indexes[0]]
        return similarity_results
    
    # 3. pass the Propmt to generate Inference
    def generate_inference(self, llm, prompt):
        try:
            output = llm(prompt, 
                        max_tokens=164, 
                        temperature = 0, 
                        top_p = 1.0)
            return output["choices"][0]["text"]
        except Exception as e:
            print(e)

    def test_model_path(self):
        return self.configs.gguf_model_path
    
    
    




if "__main__" == __name__:
#     
    chat = chat_model()
    chat.init_model()