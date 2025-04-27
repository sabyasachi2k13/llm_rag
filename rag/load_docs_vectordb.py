import pandas as pd
from bs4 import BeautifulSoup
import weaviate
from weaviate.classes.config import Configure
import urllib.request
import os
from typing import List

def word_splitter(source_text: str) -> List[str]:
    import re
    source_text = re.sub("\s+", " ", source_text)  # Replace multiple whitespces
    return re.split("\s", source_text)  # Split by single whitespace

def get_chunks_fixed_size(text: str, chunk_size: int) -> List[str]:
    text_words = word_splitter(text)
    chunks = []
    for i in range(0, len(text_words), chunk_size):
        chunk_words = text_words[i: i + chunk_size]
        chunk = " ".join(chunk_words)
        chunks.append(chunk)
    return chunks


def loadVectorDB():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    print(script_dir)
    file_path = script_dir + '\\data\\archive\\News_Category_Dataset_v3.json'
    df = pd.read_json(file_path, lines=True)

    client = weaviate.connect_to_local()
    print(client.is_ready())  # Should print: `True`

    docs = client.collections.create(
        name="collection1",
        vectorizer_config=Configure.Vectorizer.text2vec_ollama(  # Configure the Ollama embedding integration
            api_endpoint="http://host.docker.internal:11434",
            # Allow Weaviate from within a Docker container to contact your Ollama instance
            model="all-minilm",  # The model to use
        ),
        generative_config=Configure.Generative.ollama(  # Configure the Ollama generative integration
            api_endpoint="http://host.docker.internal:11434",
            # Allow Weaviate from within a Docker container to contact your Ollama instance
            model="llama3.2",  # The model to use
        )
    )

    with docs.batch.dynamic() as batch:
        for index, row in df.iterrows():
            try:
                f = urllib.request.urlopen(row["link"])
            except Exception as e:
                print(f"An error occurred: {e}")
            soup = BeautifulSoup(f.read(),"html.parser")
            docs = get_chunks_fixed_size(soup.get_text(),100)
            docs = [item for item in docs if item.strip()]
            for d in docs:
                print("document length", len(d))
                batch.add_object({
                "content": d
                })
            if batch.number_errors > 10:
                print("Batch import stopped due to excessive errors.")
                break

    client.close()  # Free up resources

if __name__ == "__main__":
    loadVectorDB()
