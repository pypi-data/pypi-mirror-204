from typing import Type, TypeVar
from langchain.vectorstores import Milvus
from abc import ABC


class MilvusVectorStore:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.client = Milvus


class ChromaVectorStore:
    pass


# Generic type variable for all vectorstores
VectorStore = type("VectorStore", (MilvusVectorStore, ChromaVectorStore), {})


SUPPORTED_VECTORSTORES = {
    "milvus": {
        "impl": MilvusVectorStore,
        "default": {"host": "localhost", "port": 19530},
    }
}


def vectorstore(
    name: str, host: str | None = None, port: int | None = None
) -> VectorStore:
    """Return a vectorstore object."""

    if name is None:
        raise RuntimeError("Impossible to instantiate a vectorstore without a name.")

    if name not in SUPPORTED_VECTORSTORES:
        raise ValueError(f"Vectorstore {name} is not supported.")

    return SUPPORTED_VECTORSTORES[name]["impl"](
        host=host or SUPPORTED_VECTORSTORES[name]["default"]["host"],
        port=port or SUPPORTED_VECTORSTORES[name]["default"]["port"],
    )
