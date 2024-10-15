import torch
from sklearn.model_selection import train_test_split
from sentence_transformers import SentenceTransformer, util
from transformers import BertTokenizer, Trainer, TrainingArguments, BertForSequenceClassification

class SimilarMedicalRequestAnalyzer:

  model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
  
  @classmethod
  def similar(cls, new_request, previous_request, threshold=0.5):
    first_embeddings = cls.model.encode(new_request, convert_to_tensor=True)
    second_embeddings = cls.model.encode(previous_request, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(first_embeddings, second_embeddings).item()
    return similarity >= threshold
