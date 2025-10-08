from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydantic_core.core_schema import none_schema

app = FastAPI()

# Pydantic model
class Book(BaseModel):
    id : int
    title : str
    author : str
    price : float
    in_stock : bool

# in-memory database
books = [
    {"id":1, "title": "Dog Days", "author": "Jeff Kinney", "price": 450.00, "in_stock": True},
    {"id":2, "name": "Captain Underpants", "author": "Dav Pilkey", "price": 550.00, "in_stock": True},
    {"id":3, "name": "Joto Kando kathmandu", "author": "Satyajit Ray", "price": 650.00, "in_stock": False}
]

# Count of books
@app.get("/books/count", status_code=200)
def count_books():
    count = len(books)
    if count > 0:
        return {"Total books": count}
    else:
        # Status code 404 is used when the list is empty
        raise HTTPException(status_code=404, detail="No books found")


# Available Books
@app.get("/books/available")
def get_available():
    available_books = []
    for i, record in enumerate(books):
        if record["in_stock"] == True:
            available_books.append(books[i])
    return {"Available books": available_books}
    raise HTTPException (status_code= 404, detail = "No books are available")

# GET all request
@app.get("/books")
def get_all():
    return {"BOOKS": books}


# POST a record
@app.post("/books", status_code=201)
def add_book(book: Book):
    present_ids = []
    for record in books:
        present_ids.append(record["id"])
    if book.dict()["id"] not in present_ids:
        if book.dict()["price"] < 0:
            raise HTTPException (status_code=400, detail="Price cannot be negative")
        else:
            books.append(book.dict())
            return {"message": "Book added successfully", "BOOK": book}
    else:
        raise HTTPException(status_code=409, detail="Book already exists")

# PUT request
@app.put("/books/{book_id}")
def update_books(book_id: int, updated_book: Book):
    for i, record in enumerate(books):
        if record["id"] == book_id:
            books[i] = updated_book.dict()
            return {"message": "Book updated successfully", "employee": books[i]}
    raise HTTPException (status_code= 404, detail = "Book not found")

# DELETE Request
@app.delete("/books/{book_id}")
def delete_student(book_id: int):
    for i, s in enumerate(books):
        if s["id"] == book_id:
            books.pop(i)
            return {"message": "Book Deleted Successfully"}
    raise  HTTPException (status_code = 404, detail= "Book not found")

# GET Book by author
@app.get("/books/search")
def get_book_filter(auth_name : str = None, price: float = None):
    for i, record in enumerate(books):
        if record["author"] == auth_name and record["price"] < price:
            return books[i]
    raise HTTPException (status_code = 404, detail = "Book Not Found")

# GET a single record
@app.get("/books/{book_id}")
def get_book(book_id: int):
    for record in books:
        if record["id"] == book_id:
            return record
    raise HTTPException(status_code=404, detail="Book not found")