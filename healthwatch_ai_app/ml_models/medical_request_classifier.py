import torch
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, Trainer, TrainingArguments, BertForSequenceClassification
  

class MedicalRequestClassifier:

  @classmethod
  def predict(cls, text):
    model = BertForSequenceClassification.from_pretrained('healthwatch_ai_app/ml_models/health_severity_model', num_labels=3)
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model.to(device)
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512).to(device)  # Move inputs to device
    outputs = model(**inputs)
    prediction = torch.argmax(outputs.logits, dim=-1)
    severity = prediction.item()
    return severity


