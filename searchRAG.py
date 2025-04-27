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

    # ner = pipeline("ner", grouped_entities=True)
    # result = ner("Sundar Pichai is the CEO of Google, based in California.")
    # for r in result:
    #     print(r)
    #
    # client = Client(
    #     host='http://127.0.0.1:11434',
    #     headers={'x-some-header': 'some-value'}
    # )
    # response = client.generate(model='llama2:latest', system="Generate Linkedin Post", prompt='Tigers of India')
    # print(response['response'])


if __name__ == "__main__":
    print('search results',search())
