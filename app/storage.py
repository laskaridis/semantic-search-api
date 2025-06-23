import logging
import qdrant_client.models as qd
from app.models import IndexRequest, SearchResult
from sentence_transformers import SentenceTransformer, CrossEncoder
from qdrant_client import QdrantClient
from typing import Any

logger = logging.getLogger(__name__)

vector_size = 384                     # Size of the vector embeddings
distance_metric = qd.Distance.COSINE  # Distance metric for similarity search
store = QdrantClient(":memory:")

bi_encoder = SentenceTransformer('./models/bi-encoder')
cross_encoder = CrossEncoder('./models/cross-encoder')

def show_collection(name: str) -> dict[str, Any] | None:
    """
    Shows the details of a specific collection in the vector store.

    Args:
        name (str): The name of the collection to show.
    Returns:
        dict: A dictionary containing the collection details.
        None: If the collection does not exist.
    Example:
        collection_details = await show_collection("my_collection")
        print(collection_details)
    """
    if store.collection_exists(collection_name=name):
        return store.get_collection(name)
    else:
        logger.error(f"Collection '{name}' does not exist.")
        return None

def list_collections() -> list[str]:
    """
    Lists all collections in the vector store.

    Returns:
        list: A list of collection names.
    Example:
        collections = await list_collections()
        print(collections)
    """
    collections = store.get_collections().collections
    return list(map(lambda collection: collection.name, collections))

def create_collection(name: str) -> bool:
    """
    Creates a new collection in the vector store. If the collection already exists,
    it will not be created again.

    Args:
        name (str): The name of the collection to create.
    Returns:
        True if the collection was created, False if it already exists.
    Example:
        await create_collection("my_collection")
    """
    if not store.collection_exists(collection_name=name):
        return store.create_collection(
            collection_name=name,
            vectors_config=qd.VectorParams(size=vector_size, distance=distance_metric)
        )
    else:
        return False

def delete_collection(name: str) -> bool:
    """
    Deletes a collection from the vector store.

    Args:
        name (str): The name of the collection to delete.
    Returns:
        True if the collection was deleted, False if it did not exist.
    Example:
        await delete_collection("my_collection")
    """
    return store.delete_collection(collection_name=name)

def vector_find(collection: str, id: str):
    """
    Finds a single item in the vector store by its external ID.

    Args:
        id (str): The external ID of the item to find.
        collection (str): The name of the collection to search in.
    Returns:
        dict: The item found in the vector store, or None if not found.
    Example:
        item = await vector_find("my_collection", "12345")
    """
    return store.scroll(
        collection_name=collection,
        scroll_filter=qd.Filter(
            must=[qd.FieldCondition(key="external_id", match=qd.MatchValue(value=id))]
        ),
        limit=1
    )[0]

def vector_index(collection: str, item: IndexRequest) -> None:
    """
    Indexes a single item into the vector store.

    Args:
        item (IndexRequest): The item to index, containing an ID and text.
        collection (str): The name of the collection to index the item into.
    Returns:
        None
    Example:
        item = IndexRequest(id="12345", text="This is a sample text.")
        await vector_index("my_collection", item)
    """
    embedding = bi_encoder.encode([item.text], normalize_embeddings=True)[0]
    result = store.upsert(
        collection_name=collection,
        points=[
            qd.PointStruct(
                id=item.id,
                vector=embedding,
                payload={"external_id":item.id, "text":item.text}
            )
        ]
    )
    logger.info(f"Indexed item with ID '{item.id}' into collection '{collection}'. Result: {result}")

def vector_search(collection: str, query: str, limit: int = 10) -> list[SearchResult]:
    """
    Searches for the most relevant items based on the query.

    Args:
        collection (str): The name of the collection to search in.
        query (str): The search query.
        limit (int): The maximum number of results to return. Default is 10.
    Returns:
        list: A list of dictionaries containing the ID, text, and score of each result.
    Example:
        results = await vector_search("my_collection", "sample query", limit=5)
        for result in results:
            print(result["id"], result["text"], result["score"])
    """
    embedding = bi_encoder.encode([query], normalize_embeddings=True)[0]
    hits = store.search(
        collection_name=collection,
        query_vector=embedding,
        limit=limit
    )
    logger.info(f"Found {len(hits)} hits for query '{query}' in collection '{collection}'.")

    if not hits:
        return []

    results = _rank(query, hits)
    return [
        SearchResult(
            id=hit.payload["external_id"],
            text=hit.payload["text"],
            score=float(score)
        )
        for hit, score in results
    ]

def _rank(query, hits) -> list[tuple[qd.PointStruct, float]]:
    """
    Ranks the results using a cross-encoder.

    Args:
        query (str): The search query.
        hits (list): The list of hits from the initial vector search.
    Returns:
        list: A sorted list of tuples containing the hit and its score.
    Example:
        results = await _rank("sample query", hits)
        for hit, score in results:
            print(hit.payload["external_id"], hit.payload["text"], score)
    """
    candidates = [(query, hit.payload["text"]) for hit in hits]
    scores = cross_encoder.predict(candidates)
    return sorted(zip(hits, scores), key=lambda x: x[1], reverse=True)

    

