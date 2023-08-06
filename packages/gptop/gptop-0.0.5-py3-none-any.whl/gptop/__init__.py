import os as _os
import pinecone as _pinecone
import openai as _openai

from .operation_utils import *
from .operation import *
from .operator import *

def init(openai_key, pinecone_key, pinecone_region, pinecone_index):
    _openai.api_key = openai_key

    _pinecone.init(
        api_key=pinecone_key,
        environment=pinecone_region
    )

    _os.environ["PINECONE_INDEX"] = pinecone_index
