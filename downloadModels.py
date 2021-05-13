from transformers import DistilBertTokenizer, TFDistilBertModel

tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = TFDistilBertModel.from_pretrained('distilbert-base-uncased')

model_file = "./model/distilBERT"
tokenizer_file = "./model/distilTokenizer"

model.save_pretrained(model_file)
tokenizer.save_pretrained(tokenizer_file)
