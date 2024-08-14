from pymongo import MongoClient

client = MongoClient("mongodb+srv://root:toor@sample.950g6.mongodb.net/?retryWrites=true&w=majority&appName=sample")
restaurant_collection = client.sample_restaurants.restaurants

