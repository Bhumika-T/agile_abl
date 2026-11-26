from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Book

from .forms import clean_book_form

bp = Blueprint("books", __name__, url_prefix="/books")


@bp.get("/")
def list_books():
    q = request.args.get("q", "").strip()

    query = Book.query

    if q:
        pattern = f"%{q}%"
        query = query.filter(
            or_(
                Book.title.ilike(pattern),
                Book.author.ilike(pattern),
                Book.book_code.ilike(pattern),
                Book.isbn.ilike(pattern),
            )
        )

    books = query.order_by(Book.title.asc()).all()

    return render_template("books/list.html", books=books, q=q)


@bp.route("/add", methods=["GET", "POST"])
def add_book():
    errors = {}
    form = request.form if request.method == "POST" else {}

    if request.method == "POST":
        values, errors = clean_book_form(request.form)

        if not errors:
            book = Book(
                book_code=Book.next_book_code(),
                **values
            )
            db.session.add(book)

            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                errors["isbn"] = "This ISBN already exists."
            else:
                flash(f"{book.title} added successfully.", "success")
                return redirect(url_for("books.list_books"))

    return render_template(
        "books/form.html",
        mode="add",
        book=None,
        form=form,
        errors=errors,
    )


@bp.get("/<int:book_id>")
def detail(book_id):
    book = db.get_or_404(Book, book_id)
    return render_template("books/detail.html", book=book)


@bp.route("/<int:book_id>/edit", methods=["GET", "POST"])
def edit_book(book_id):
    book = db.get_or_404(Book, book_id)
    errors = {}
    form = request.form if request.method == "POST" else {}

    if request.method == "POST":
        values, errors = clean_book_form(request.form, book=book)

        if not errors:
            for field, value in values.items():
                setattr(book, field, value)

            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                errors["isbn"] = "This ISBN already exists."
            else:
                flash(f"{book.title} updated successfully.", "success")
                return redirect(url_for("books.detail", book_id=book.id))

    return render_template(
        "books/form.html",
        mode="edit",
        book=book,
        form=form,
        errors=errors,
    )


@bp.post("/<int:book_id>/delete")
def delete_book(book_id):
    book = db.get_or_404(Book, book_id)
    db.session.delete(book)
    db.session.commit()

    flash(f"{book.title} deleted successfully.", "success")
    return redirect(url_for("books.list_books"))
