# 📄 Document Summarizer & Q&A App

A powerful and easy-to-use **Streamlit web application** that allows users to upload documents, generate summaries using Pegasus Large, and chat with the content using a Tiny Llama model. This project leverages Hugging Face Transformers, FAISS, and local GGUF models via `llama.cpp`.

---

## 🚀 Features

- 📝 **Document Upload** – Upload PDFs or text files.
- 📚 **Text Summarization** – Generate high-quality summaries using Pegasus Large.
- 💬 **Chat with Document** – Ask questions about the content using Tiny Llama (GGUF).
- ⚡ **Fast Search** – Uses FAISS for vector similarity retrieval.
- 🧠 **Local Inference** – Runs on local models using `llama-cpp-python`.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **LLMs**: Pegasus Large, Tiny Llama (GGUF)
- **Embedding**: Hugging Face Embedding models
- **Vector Store**: FAISS
- **Quantization**: GGUF for Tiny Llama
- **Backend**: Python

---

## 📦 Installation

```bash
git clone https://github.com/Himanshu-manjrekar/Document_SummarizationQandA
cd Document_SummarizationQandA
pip install -r requirements.txt
```

---

##  Steps to carry after Installation

- **Download Tiny-llama-gguf**: url: https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF
- **Move the GGUF file**: move to downloaded gguf file to `src/components/artifacts/models/tiny_llama/`

---

## ▶️ Run the App
```bash
streamlit run app.py
```

---

## 📸 Application Screenshots

- **🖼️ Application UI**: 
<img src="src\components\app_images\1.PNG" alt="Application UI"> 

- **🖼️ Chat Q&A**:
<img src="src\components\app_images\5.PNG" alt="Chat Q&A">

- **🖼️ Summarization**:
<img src="src\components\app_images\7.PNG" alt="Summarization">

---

## 🧑‍💻 Author
Himanshu Manjrekar