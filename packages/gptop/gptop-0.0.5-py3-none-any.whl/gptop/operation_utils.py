import os as _os
import json as _json
from uuid import uuid4 as _uuid4
import pinecone as _pinecone
from openai.embeddings_utils import get_embedding as _get_embedding
from .operation import Operation as _Operation


class Utils():
    """
    A set of utility objects for managing operations
    """

    @classmethod
    def create_operation(self, namespace, type, name, description,
                         url, path, requires_auth, schema):
        """
        Creates an operation, creates an embedding from it, and
        stores it in a vector database.
        - namespace: The namespace to store the embedding
        - type: The type of operation
        - url: The url of the operation
        - path: The path to the operation
        - requires_auth: If the operation requires authentication
        - schema: The schema of the operation

        Also writes the operation ID to the `ops_list.txt` file

        Returns: The created operation
        """

        index = _pinecone.Index(_os.getenv("PINECONE_INDEX"))

        id = str(_uuid4())

        operation = _Operation(
            id=id,
            type=type,
            name=name,
            description=description,
            url=url,
            path=path,
            requires_auth=requires_auth,
            schema=_json.dumps(_json.loads(schema), separators=(',', ': '))
        )

        embedding = _get_embedding(operation.embedding_obj(),
                                  engine="text-embedding-ada-002")

        to_upsert = zip([id], [embedding], [operation.metadata()])

        index.upsert(vectors=list(to_upsert), namespace=namespace)

        return operation

    @classmethod
    def get_operation(self, namespace: str, id: str):
        """
        Fetches an existing operation from the vector database.
        - namespace: The namespace to store the embedding
        - id: The identifier of the operation

        Returns: The operation represented
        """
        index = _pinecone.Index(_os.getenv("PINECONE_INDEX"))

        result = index.fetch([id], namespace=namespace)
        vectors = result.get('vectors')
        vector = vectors.get(id)

        if not vector:
            return None

        obj = vector.get('metadata')
        return _Operation.from_obj(obj)

    @classmethod
    def update_operation(self, namespace, id, type, name, description,
                         url, path, requires_auth, schema):
        """
        Updates an existing operation, creates a new embedding, and
        overrides the existing operation in the vector database.
        - namespace: The namespace to store the embedding
        - id: The identifier of the operation
        - type: The type of operation
        - url: The url of the operation
        - path: The path to the operation
        - requires_auth: If the operation requires authentication
        - schema: The schema of the operation

        Returns: The updated operation
        """

        operation = _Operation(
            id=id,
            type=type,
            name=name,
            description=description,
            url=url,
            path=path,
            requires_auth=requires_auth,
            schema=_json.dumps(_json.loads(schema), separators=(',', ': '))
        )

        index = _pinecone.Index(_os.getenv("PINECONE_INDEX"))

        embedding = _get_embedding(operation.embedding_obj(),
                                  engine="text-embedding-ada-002")

        to_upsert = zip([id], [embedding], [operation.metadata()])

        index.upsert(vectors=list(to_upsert), namespace=namespace)

        return operation

    @classmethod
    def remove_operation(self, namespace: str, id: str):
        """
        Removes an existing operation from the vector database.
        - namespace: The namespace to store the embedding
        - id: The identifier of the operation

        Also removes the operation ID from `ops_list.txt` file.
        """

        index = _pinecone.Index(_os.getenv("PINECONE_INDEX"))

        index.delete(ids=[id], namespace=namespace)

    @classmethod
    def remove_namespace(self, namespace: str):
        """
        [DANGEROUS] Deletes an entire namespace of operations.
        - namespace: The namespace in the vector database
        """
        index = _pinecone.Index(_os.getenv("PINECONE_INDEX"))

        index.delete(deleteAll='true', namespace=namespace)
