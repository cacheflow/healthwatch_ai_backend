import torch
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, Trainer, TrainingArguments, BertForSequenceClassification
import os
from huggingface_hub import login
from django.conf import settings

import requests

class MedicalRequestClassifier:

  @classmethod
  def predict(cls, text):
    API_URL = settings.HUGGINGFACE_INFERENCE_URL
    headers = {
      "Accept" : "application/json",
      "Authorization": f"Bearer {settings.HUGGINGFACE_TOKEN}",
      "Content-Type": "application/json" 
    }
    response = requests.post(API_URL, headers=headers, json={
      "inputs": text,
      "parameters": {}
    })
    return response.json()


