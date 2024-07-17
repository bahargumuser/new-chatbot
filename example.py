import pandas as pd
import torch
from transformers import Trainer, TrainingArguments, AutoModelForSequenceClassification, AutoTokenizer
from datasets import Dataset

def train_bert_model(data_path):
    # JSON dosyasından veri yükleme
    with open(data_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # JSON verisini Pandas DataFrame'e dönüştürme
    df = pd.DataFrame(data)

    # DataFrame'i Hugging Face Dataset formatına dönüştürme
    dataset = Dataset.from_pandas(df)

    # Model ve tokenizer yükleme
    model_name = "bert-base-uncased"
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Veri setini token'lara çevirme fonksiyonu
    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True)

    tokenized_datasets = dataset.map(tokenize_function, batched=True)

    # Eğitim argümanlarını ayarlama
    training_args = TrainingArguments(
        output_dir="./results",
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01,
    )

    # Trainer oluşturma
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["test"],  # Opsiyonel: Test veri seti
    )

    # Model eğitimi
    trainer.train()

    # Eğitilen modeli kaydetme
    model.save_pretrained("./bert-chatbot-model")

if __name__ == "__main__":
    data_path = "./responses.json"  # Veri dosyasının yolu
    train_bert_model(data_path)