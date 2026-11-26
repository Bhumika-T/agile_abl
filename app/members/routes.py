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
from app.models import MEMBERSHIP_TYPES, Member

from .forms import clean_member_form

bp = Blueprint("members", __name__, url_prefix="/members")


@bp.get("/")
def list_members():
    q = request.args.get("q", "").strip()
    status = request.args.get("status", "All")

    query = Member.query
    if q:
        pattern = f"%{q}%"
        query = query.filter(
            or_(
                Member.full_name.ilike(pattern),
                Member.email.ilike(pattern),
                Member.member_code.ilike(pattern),
            )
        )
    if status in ("Active", "Inactive"):
        query = query.filter(Member.status == status)

    members = query.order_by(Member.joined_on.desc(), Member.id.asc()).all()
    stats = {
        "total": Member.query.count(),
        "active": Member.query.filter_by(status="Active").count(),
        "inactive": Member.query.filter_by(status="Inactive").count(),
    }
    return render_template(
        "members/list.html", members=members, q=q, status=status, stats=stats
    )


@bp.route("/register", methods=["GET", "POST"])
def register():
    errors = {}
    form = request.form if request.method == "POST" else {}

    if request.method == "POST":
        values, errors = clean_member_form(request.form)
        if not errors:
            member = Member(member_code=Member.next_member_code(), **values)
            db.session.add(member)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                errors["email"] = "A member with this email is already registered."
            else:
                flash(
                    f"{member.full_name} registered as {member.member_code}.",
                    "success",
                )
                return redirect(url_for("members.detail", member_id=member.id))

    return render_template(
        "members/form.html",
        mode="register",
        member=None,
        form=form,
        errors=errors,
        membership_types=MEMBERSHIP_TYPES,
    )


@bp.get("/<int:member_id>")
def detail(member_id):
    member = db.get_or_404(Member, member_id)
    return render_template("members/detail.html", member=member)


@bp.route("/<int:member_id>/edit", methods=["GET", "POST"])
def edit(member_id):
    member = db.get_or_404(Member, member_id)
    errors = {}
    form = request.form if request.method == "POST" else {}

    if request.method == "POST":
        values, errors = clean_member_form(request.form, member=member)
        if not errors:
            for field, value in values.items():
                setattr(member, field, value)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                errors["email"] = "A member with this email is already registered."
            else:
                flash(f"{member.full_name}'s details were updated.", "success")
                return redirect(url_for("members.detail", member_id=member.id))

    return render_template(
        "members/form.html",
        mode="edit",
        member=member,
        form=form,
        errors=errors,
        membership_types=MEMBERSHIP_TYPES,
    )


@bp.post("/<int:member_id>/toggle-status")
def toggle_status(member_id):
    member = db.get_or_404(Member, member_id)
    member.status = "Inactive" if member.status == "Active" else "Active"
    db.session.commit()
    flash(f"{member.full_name} is now {member.status.lower()}.", "success")
    return redirect(url_for("members.detail", member_id=member.id))
