import openai
import os
import requests
import numpy as np
import pandas as pd
from typing import Iterator
import tiktoken
import textract
from numpy import array, average

from database import get_redis_connection

from config import VECTOR_DIM, VECTOR_FIELD_NAME, DISTANCE_METRIC, INDEX_NAME, PREFIX

# Setup Redis
from redis import Redis
from redis.commands.search.query import Query
from redis.commands.search.field import (
    TextField,
    VectorField,
    NumericField
)
from redis.commands.search.indexDefinition import (
    IndexDefinition,
    IndexType
)

# The transformers.py file contains all of the transforming functions, including ones to chunk, embed and load data
# For more details the file and work through each function individually
from transformers import handle_file_string

# Set our default models and chunking size
from config import COMPLETIONS_MODEL, EMBEDDINGS_MODEL, CHAT_MODEL, TEXT_EMBEDDING_CHUNK_SIZE, VECTOR_FIELD_NAME

# Ignore unclosed SSL socket warnings - optional in case you get these errors
import warnings

warnings.filterwarnings(action="ignore", message="unclosed", category=ImportWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning) 

pd.set_option('display.max_colwidth', 0)

data_dir = os.path.join(os.curdir,'example-chatbot/PDFs')
pdf_files = sorted([x for x in os.listdir(data_dir) if 'DS_Store' not in x])
print(pdf_files)

# Get a Redis connection
redis_client = get_redis_connection()

# Define RediSearch fields for each of the columns in the dataset
# This is where you should add any additional metadata you want to capture
filename = TextField("filename")
text_chunk = TextField("text_chunk")
file_chunk_index = NumericField("file_chunk_index")

# define RediSearch vector fields to use HNSW index
text_embedding = VectorField(VECTOR_FIELD_NAME,
    "HNSW", {
        "TYPE": "FLOAT32",
        "DIM": VECTOR_DIM,
        "DISTANCE_METRIC": DISTANCE_METRIC
    }
)

# Add all our field objects to a list to be created as an index
fields = [filename,text_chunk,file_chunk_index,text_embedding]


# Optional step to drop the index if it already exists
#redis_client.ft(INDEX_NAME).dropindex()

# Check if index exists
try:
    redis_client.ft(INDEX_NAME).info()
    print("Index already exists")
except Exception as e:
    print(e)
    # Create RediSearch Index
    print('Not there yet. Creating')
    redis_client.ft(INDEX_NAME).create_index(
        fields = fields,
        definition = IndexDefinition(prefix=[PREFIX], index_type=IndexType.HASH)
    )

# Initialise tokenizer
tokenizer = tiktoken.get_encoding("cl100k_base")

# Process each PDF file and prepare for embedding
for pdf_file in pdf_files:
    
    pdf_path = os.path.join(data_dir,pdf_file)
    print(pdf_path)
    
    # Extract the raw text from each PDF using textract
    text = textract.process(pdf_path, method='pdfminer')
    
    # Chunk each document, embed the contents and load to Redis
    handle_file_string((pdf_file,text.decode("utf-8")),tokenizer,redis_client,VECTOR_FIELD_NAME,INDEX_NAME)

# Check that our docs have been inserted
print(redis_client.ft(INDEX_NAME).info()['num_docs'])