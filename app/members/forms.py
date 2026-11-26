import re

from app.extensions import db
from app.models import MEMBERSHIP_TYPES, Member

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$")
PHONE_CHARS_RE = re.compile(r"^[0-9+()\-\s]{7,20}$")


def clean_member_form(form, member=None):
    values = {
        "full_name": (form.get("full_name") or "").strip(),
        "email": (form.get("email") or "").strip().lower(),
        "phone": (form.get("phone") or "").strip(),
        "address": (form.get("address") or "").strip(),
        "membership_type": (form.get("membership_type") or "Student").strip(),
    }
    errors = {}

    if not values["full_name"]:
        errors["full_name"] = "Full name is required."
    elif len(values["full_name"]) > 120:
        errors["full_name"] = "Full name must be 120 characters or fewer."

    if not values["email"]:
        errors["email"] = "Email is required."
    elif not EMAIL_RE.match(values["email"]):
        errors["email"] = "Enter a valid email address."
    else:
        query = Member.query.filter(db.func.lower(Member.email) == values["email"])
        if member is not None:
            query = query.filter(Member.id != member.id)
        if query.first() is not None:
            errors["email"] = "A member with this email is already registered."

    digits = re.sub(r"\D", "", values["phone"])
    if not values["phone"]:
        errors["phone"] = "Phone number is required."
    elif not PHONE_CHARS_RE.match(values["phone"]) or not 7 <= len(digits) <= 15:
        errors["phone"] = "Enter a valid phone number with 7 to 15 digits."

    if len(values["address"]) > 255:
        errors["address"] = "Address must be 255 characters or fewer."

    if values["membership_type"] not in MEMBERSHIP_TYPES:
        errors["membership_type"] = "Choose a valid membership type."

    return values, errors
