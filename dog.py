import requests

def dog():
    r = requests.post("http://dog.ceo/api/breeds/image/random")
    print(r.json())
    return "respond with GOODBOYE or NOTHX || " + r.json()['message']

def goodboye():
    return 1

def nothx():
    return -1