# to_paragraphs

> Note, the code is currently ~slow and messy. It's a work in progress.

Extracts paragraphs from a string, using the semantic similarity between sentences to determine paragraph boundaries.
This tends to work better than the naive approach of splitting on newlines.

## Installation

```bash
pip install to_paragraphs
```

## Example

```python
from to_paragraphs import to_paragraphs

text = """
The biosphere includes everything living on Earth it is also known as ecosphere. Currently the biosphere has a biomass (or amount of living things) at around 1900 gigatonnes of carbon. It is not certain exactly how thick the biosphere is, though scientists predict that it is around 12,500 meters. The biosphere extends to the upper areas of the atmosphere, including birds and insects. 
Pizza is an Italian food that was created in Italy (The Naples area). It is made with different toppings. Some of the most common toppings are cheese, sausages, pepperoni, vegetables, tomatoes, spices and herbs and basil. These toppings are added over a piece of bread covered with sauce. The sauce is most often tomato-based, but butter-based sauces are used, too. The piece of bread is usually called a "pizza crust". Almost any kind of topping can be put over a pizza. The toppings used are different in different parts of the world. Pizza comes from Italy from Neapolitan cuisine. However, it has become popular in many parts of the world.
"""


def embed_fn(content):
    # ... some function that returns an embedding for a string
    pass


paragraphs = to_paragraphs(text, embed_fn=embed_fn)

for paragraph in paragraphs:
    print(paragraph)  # prints the paragraph about the biosphere, then the paragraph about pizza
```

### Example embedding function

```python
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel

CACHE_PATH = '/tmp/transformers'
TOKENIZER = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2', cache_dir=CACHE_PATH)
MODEL = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2', cache_dir=CACHE_PATH)


def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


def embed(sentences):
    encoded_input = TOKENIZER(sentences, padding=True, truncation=True, return_tensors='pt')

    with torch.no_grad():
        model_output = MODEL(**encoded_input)

    sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])

    return F.normalize(sentence_embeddings, p=2, dim=1)
```
