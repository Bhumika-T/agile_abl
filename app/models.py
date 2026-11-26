from datetime import date, datetime

from .extensions import db

MEMBERSHIP_TYPES = ("Student", "Faculty", "Public")
MEMBER_STATUSES = ("Active", "Inactive")


class Member(db.Model):
    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True)
    member_code = db.Column(db.String(12), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False, default="")
    membership_type = db.Column(db.String(20), nullable=False, default="Student")
    status = db.Column(db.String(10), nullable=False, default="Active")
    joined_on = db.Column(db.Date, nullable=False, default=date.today)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        db.CheckConstraint(
            "status IN ('Active', 'Inactive')", name="ck_members_status"
        ),
        db.CheckConstraint(
            "membership_type IN ('Student', 'Faculty', 'Public')",
            name="ck_members_membership_type",
        ),
    )

    @property
    def initials(self):
        parts = [part for part in self.full_name.split() if part]
        return "".join(part[0] for part in parts[:2]).upper() or "?"

    @classmethod
    def next_member_code(cls):
        last = cls.query.order_by(cls.id.desc()).first()
        if last is None:
            return "MEM-0001"
        try:
            current = int(last.member_code.split("-")[1])
        except (IndexError, ValueError):
            current = cls.query.count()
        return f"MEM-{current + 1:04d}" 


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    book_code = db.Column(db.String(12), unique=True, nullable=False)
    title = db.Column(db.String(150), nullable=False, index=True)
    author = db.Column(db.String(120), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    publisher = db.Column(db.String(120), nullable=False, default="")
    category = db.Column(db.String(80), nullable=False, default="")
    total_copies = db.Column(db.Integer, nullable=False, default=1)
    available_copies = db.Column(db.Integer, nullable=False, default=1)

        created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
        )


       __table_args__ = (
        db.CheckConstraint(
            "total_copies >= 0",
            name="ck_books_total_copies"
        ),
        db.CheckConstraint(
            "available_copies >= 0 AND available_copies <= total_copies",
            name="ck_books_available_copies"
        ),
       )


    @classmethod
    def next_book_code(cls):
        last = cls.query.order_by(cls.id.desc()).first()

        if last is None:
            return "BOOK-0001"

        try:
            current = int(last.book_code.split("-")[1])
        except (IndexError, ValueError):
            current = cls.query.count()

        return f"BOOK-{current + 1:04d}"
















