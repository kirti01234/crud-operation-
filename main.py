
from fastapi import FastAPI, HTTPException
from bson import ObjectId

from database import books_collection
from models import Book

app = FastAPI()


# CREATE
@app.post("/books")
def create_book(book: Book):

    result = books_collection.insert_one(book.dict())

    return {
        "message": "Book Created",
        "id": str(result.inserted_id)
    }

@app.get("/books")
def get_books():

    books = []

    for book in books_collection.find():

        books.append({
            "id":book["id"],
            "title": book["title"],
            "author": book["author"],
            "price": book["price"]
        })

    return books


# READ ONE
@app.get("/books/{book_id}")
def get_book(book_id: str):

    book = books_collection.find_one({"_id": ObjectId(book_id)})

    if not book:
        raise HTTPException(status_code=404, detail="Book Not Found")

    return {
        "id": book["_id"],
        "title": book["title"],
        "author": book["author"],
        "price": book["price"]
    }


# UPDATE
@app.put("/books/{book_id}")
def update_book(book_id: str, book: Book):

    result = books_collection.update_one(
        {"id": ObjectId(book_id)},
        {"$set": book.dict()}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Book Not Found")

    return {"message": "Book Updated"}


# DELETE
@app.delete("/books/{book_id}")
def delete_book(book_id:str):
    return {"message":"deleted"}


@app.get("/")
def home():
    return {"message":"API Running"}
    