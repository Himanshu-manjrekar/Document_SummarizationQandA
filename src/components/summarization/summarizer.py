# Code to Initialize Document, Quantize it and save the summarizer model (One time run)

import os
from transformers import pipeline, AutoTokenizer
# from optimum.intel import INCQuantizer, INCConfig, INCModelForSeq2SeqLM
# from optimum.intel.neural_compressor import 
from dataclasses import dataclass



@dataclass
class summarizer_model_config:
    model_task: str = "summarization"
    model_repo_id: str = "google/pegasus-large"
    model_path: str = os.path.join("artifacts\\models\\pegasus", "summarizer_model")
    tokenizer_path = os.path.join("artifacts\\models\\pegasus", "tokenizer_model")
    # model_repo_id: str = "sshleifer/distilbart-cnn-12-6"

# class summarizer_model:
#     def __init__(self):
#         self.configs = summarizer_model_config()

#     def initialize_model(self): 
#         try:
#             tokenizer = AutoTokenizer.from_pretrained(self.configs.model_repo_id)
#             summarizer_model = INCModelForSeq2SeqLM.from_pretrained(self.configs.model_repo_id)
#             return summarizer_model, tokenizer
#         except Exception as e:
#             print("Error Occured While inititlizing the model")
#             print(e)
    
#     def quantize_model(self, model):
#         try:
#             # Defining Quantization config
#             quantization_config = PostTrainingQuantConfig(approach="dynamic")

#             # Quantizer instance
#             quantizer = INCQuantizer.from_pretrained(model)

#             # Quantize the model
#             print("Saving the quantized model")
#             quantizer.quantize(
#                 save_directory="E:\\Python\\AI_Projects\\Documment_summarization_q_a\\artifacts\\models\\pegasus",  # Path where model will be saved
#                 quantization_config=quantization_config,
#             )
#             print("Quantized Model saved Successfully")
#         except Exception as e:
#             print("Something went wrong while quantizing the model")
#             print(e)

#     def save_model(self, tokenizer):
#         try:
#             # save tokenizer
#             print("Saving Tokenizer model") 
#             tokenizer.save_pretrained("E:\\Python\\AI_Projects\\Documment_summarization_q_a\\artifacts\\models\\tokenizer")
#             print("Tokenizer saved Successfully")
#         except Exception as e:
#             print("Something went wrong while saving tokenizer")
    
class summarizer_model:
    def __init__(self):
        self.configs = summarizer_model_config()
    def summarize_the_data(self, model, extracted_chunks):
        # Take the Extracted text and Summarize the data
        try:
            summary = []
            for chunk in extracted_chunks:
                actual_len = len(chunk.split())
                max_len = max(80, int(actual_len * 0.5))
                result = model(chunk, max_length = max_len)[0]["summary_text"]
                summary.append(result)
                summaries = " ".join(summary)
            return summaries
        except Exception as e:
            print("Error Occured while summarizing the data")
            print(e)



# if __name__ == "__main__":
#     # print(tf.__version__)
#     summarizer = summarizer()
#     # Extract PDF
#     document = extract_pdf("E:\\Python\\AI_Projects\\Documment_summarization_q_a\\artifacts\\data\\attention.pdf")
#     # Clean document
#     cleaned_document = clean_text(document)
#     # Create Chunks
#     chunks = chunks_of_text(cleaned_document)

#     # summarize the document
#     summarizer.summarize_the_data(chunks)





if __name__ == "__main__":
    summ_model = summarizer_model()
    model = summ_model.initialize_model()
    summ_model.quantize_model(model[0])
    # summ_model.save_model(model[1])
