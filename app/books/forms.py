
from app.extensions import db
from app.models import Book


def clean_book_form(form, book=None):
    values = {
        "title": (form.get("title") or "").strip(),
        "author": (form.get("author") or "").strip(),
        "isbn": (form.get("isbn") or "").strip(),
        "publisher": (form.get("publisher") or "").strip(),
        "category": (form.get("category") or "").strip(),
    }

    errors = {}

    if not values["title"]:
        errors["title"] = "Book title is required."
    elif len(values["title"]) > 150:
        errors["title"] = "Title must be 150 characters or fewer."

    if not values["author"]:
        errors["author"] = "Author name is required."
    elif len(values["author"]) > 120:
        errors["author"] = "Author name must be 120 characters or fewer."

    if not values["isbn"]:
        errors["isbn"] = "ISBN is required."
    elif len(values["isbn"]) > 20:
        errors["isbn"] = "ISBN must be 20 characters or fewer."
    else:
        query = Book.query.filter(
            db.func.lower(Book.isbn) == values["isbn"].lower()
        )

        if book is not None:
            query = query.filter(Book.id != book.id)

        if query.first() is not None:
            errors["isbn"] = "A book with this ISBN already exists."

    if len(values["publisher"]) > 120:
        errors["publisher"] = "Publisher name is too long."

    if len(values["category"]) > 80:
        errors["category"] = "Category must be 80 characters or fewer."

    for field in ("total_copies", "available_copies"):
        raw_value = (form.get(field) or "1").strip()

        try:
            values[field] = int(raw_value)
            if values[field] < 0:
                errors[field] = "Copies cannot be negative."
        except ValueError:
            values[field] = 0
            errors[field] = "Enter a valid whole number."

    if (
        "total_copies" not in errors
        and "available_copies" not in errors
        and values["available_copies"] > values["total_copies"]
    ):
        errors["available_copies"] = (
            "Available copies cannot exceed total copies."
        )

    return values, errors
