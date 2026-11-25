from flask import Blueprint, render_template

from app.models import Member

bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    member_counts = {
        "total": Member.query.count(),
        "active": Member.query.filter_by(status="Active").count(),
        "inactive": Member.query.filter_by(status="Inactive").count(),
    }
    return render_template("index.html", member_counts=member_counts)
