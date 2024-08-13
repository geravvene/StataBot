from pymongo import MongoClient

def connect(name):
    client = MongoClient("mongodb+srv://geravvene:NJxN8XPdTKMe84YF@wordigma.rmxf6nd.mongodb.net/")
    db = client['StataBot']
    collection = db[name]
    return collection