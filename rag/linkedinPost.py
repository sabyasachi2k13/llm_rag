from ollama import Client

def generatePost(texttopost: str):
    client = Client(
        host='http://127.0.0.1:11434',
        headers={'x-some-header': 'some-value'}
    )
    response = client.generate(model='llama2', system="Generate a linkedin post, make it interesting", prompt=texttopost)
    return response.response

