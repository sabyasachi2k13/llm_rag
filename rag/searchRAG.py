import weaviate

def search(query: str):
    client = weaviate.connect_to_local()
    collection = client.collections.get("collection1")

    response = collection.query.hybrid(
        query=query,  # The model provider integration will automatically vectorize the query
        limit=10
    )
    combined_text = "\n\n".join(
        [obj.properties.get("content", "") for obj in response.objects]
    )

    client.close()  # Free up resources
    return combined_text

