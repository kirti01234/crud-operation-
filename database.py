from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client.library_db

books_collection = db.books
