import streamlit as st
import re
import torch 

from PyPDF2 import PdfReader
from docx import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dataclasses import dataclass

torch.classes.__path__ = []

@dataclass
class utilities_config:
    pdf_file_type : str = "application/pdf"
    txt_file_type : str = "text/plain"
    dox_file_type : str = "application/vnd.openxmlformats-officedocument.wordprocessingml.document" 
    text_decode_type: str = "utf-8"


class utilities:
    def __init__(self):
        self.configs = utilities_config()

    # Extract PDF's
    def extract_pdf(self, uploaded_file):
    # doc = fitz.open(file_path)
        doc = PdfReader(uploaded_file)
        text = ""
        for page in doc.pages:
            text += page.extract_text()
        return text

    # Extract Docx Files
    def extract_doc(self, uploaded_file):
        doc = Document(uploaded_file)
        text = "\n".join([data.text for data in doc.paragraphs])
        return text

    # Extract txt Files
    def extract_txt(self, uploaded_file):
        data = uploaded_file.read().decode(self.configs.text_decode_type)
        return data

    # Cleaning the extracted text
    def clean_text(self, text):
        # Replace multiple newlines with a single newline (preserves paragraphs)
        text = re.sub(r"\n{2,}", "\n", text)  # Remove extra spaces and just spaces between two words
        text = re.sub(r"(?<!\n)\n(?!\n)", " ", text) # Remove extra line speprators
        text  = re.sub(r'[^\x00-\x7F]+', " ", text) ## hyper links are highlighted as "\xa0" so we will remove this
        text = re.sub(r'\b(?:[A-Za-z0-9]\.\s*)+(?=\s)', '', text) # Pattern to match sequences like A. or A.1. or a.1.2. followed by a space
        return text

    # making chunks of 1000 words with overlap of 50 words
    def chunks_of_text(self, extracted_text):
        cleaned_text = self.clean_text(extracted_text)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)
        chunks = text_splitter.split_text(cleaned_text)
        # print("length of chunks:- ", len(chunks))
        return chunks

    # clean context
    def clean_context(self, context):
        cleaned_context = re.sub(' +', ' ', context)
        return cleaned_context

    def Operation_handler(self, file):
        # First we will check the file type and execute the appropriate I/O operation
        if file.type == self.configs.pdf_file_type: # PDF File
            text = self.extract_pdf(file)   # This will return the text
            chunks = self.chunks_of_text(text)
            return chunks
        elif file.type == self.configs.txt_file_type:  # TXT files
            text = self.extract_txt(file)
            chunks = self.chunks_of_text(text)
            return chunks
        elif file.type == self.configs.dox_file_type:  # DOCX files
            text = self.extract_doc(file)
            chunks = self.chunks_of_text(text)
            return chunks
        else:
            return None # we need to handle this in Future
        
    

    