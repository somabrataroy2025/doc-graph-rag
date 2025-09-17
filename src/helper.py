from common.llm import embedding
from typing import Any
import pandas as pd
    
def embed_text(txt:str)->Any| None:
    if txt:
        return embedding.embed_query(txt)
    else:
        return None

def split_dataframe(df, chunk_size = 100):
    chunks = list()
    num_chunks = len(df) // chunk_size + 1
    for i in range(num_chunks):
        chunks.append(df[i*chunk_size:(i+1)*chunk_size])
    return chunks