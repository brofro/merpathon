import requests

def dog():
    r = requests.post("http://dog.ceo/api/breeds/image/random")
    print(r.json())
    return r.json()['message']