from transformers import BartTokenizer, BartModel
import torch

def get_avg_embedding(sentence):
    model_name = 'facebook/bart-base'
    model = BartModel.from_pretrained(model_name)
    tokenizer = BartTokenizer.from_pretrained(model_name)

    # Tokenize the sentence
    inputs = tokenizer(sentence, return_tensors='pt', truncation=True, padding=True)

    # Get the model outputs
    with torch.no_grad():
        outputs = model(**inputs)

    # Retrieve the last hidden state of the encoder
    last_hidden_state = outputs.last_hidden_state

    # Average the embeddings across the tokens to get a single sentence-level embedding
    avg_embedding = torch.mean(last_hidden_state, dim=1).squeeze()

    return avg_embedding