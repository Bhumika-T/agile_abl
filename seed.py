"""Populate the development database with sample members."""
from datetime import date

from app import create_app
from app.extensions import db
from app.models import Member

SAMPLES = [
    ("MEM-0001", "Asha Rao", "asha.rao@example.com", "+91 98765 43210",
     "12 MG Road, Bengaluru", "Student", "Active", date(2024, 6, 12)),
    ("MEM-0002", "Rahul Menon", "rahul.menon@example.com", "+91 90000 12345",
     "44 Residency Road, Bengaluru", "Faculty", "Active", date(2024, 8, 3)),
    ("MEM-0003", "Priya Iyer", "priya.iyer@example.com", "+91 98801 23456",
     "7 Park Street, Mysuru", "Public", "Active", date(2025, 1, 21)),
    ("MEM-0004", "Vikram Shetty", "vikram.shetty@example.com", "+91 97400 55678",
     "203 Lake View, Mangaluru", "Student", "Inactive", date(2025, 3, 9)),
    ("MEM-0005", "Meera Nair", "meera.nair@example.com", "+91 96320 88910",
     "18 Temple Road, Kochi", "Faculty", "Active", date(2025, 5, 27)),
    ("MEM-0006", "Arjun Desai", "arjun.desai@example.com", "+91 99860 77123",
     "5 College Lane, Hubballi", "Student", "Active", date(2025, 9, 14)),
]


def main():
    app = create_app()
    with app.app_context():
        if Member.query.count():
            print(f"Members already exist ({Member.query.count()}); nothing to seed.")
            return

        for code, full_name, email, phone, address, membership_type, status, joined_on in SAMPLES:
            db.session.add(
                Member(
                    member_code=code,
                    full_name=full_name,
                    email=email,
                    phone=phone,
                    address=address,
                    membership_type=membership_type,
                    status=status,
                    joined_on=joined_on,
                )
            )
        db.session.commit()
        print(f"Seeded {len(SAMPLES)} members.")


if __name__ == "__main__":
    main()
