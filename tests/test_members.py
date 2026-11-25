import pytest
from sqlalchemy.pool import StaticPool

from app import create_app
from app.extensions import db
from app.models import Member


@pytest.fixture()
def app():
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret",
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "SQLALCHEMY_ENGINE_OPTIONS": {
                "connect_args": {"check_same_thread": False},
                "poolclass": StaticPool,
            },
        }
    )
    with app.app_context():
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def member_payload(**overrides):
    payload = {
        "full_name": "Asha Rao",
        "email": "asha.rao@example.com",
        "phone": "+91 98765 43210",
        "address": "12 MG Road, Bengaluru",
        "membership_type": "Student",
    }
    payload.update(overrides)
    return payload


def register(client, **overrides):
    return client.post(
        "/members/register", data=member_payload(**overrides), follow_redirects=True
    )


def test_home_and_directory_render(client):
    assert client.get("/").status_code == 200
    assert client.get("/members/").status_code == 200


def test_register_member_creates_record(client, app):
    response = register(client)
    html = response.get_data(as_text=True)

    with app.app_context():
        member = Member.query.one()
        assert member.member_code == "MEM-0001"
        assert member.email == "asha.rao@example.com"
        assert member.status == "Active"
        assert member.membership_type == "Student"
        assert member.joined_on is not None

    assert "MEM-0001" in html
    assert "registered" in html.lower()


def test_duplicate_email_is_rejected_case_insensitively(client, app):
    register(client)
    response = register(client, email="ASHA.RAO@example.com")

    assert b"already registered" in response.data
    with app.app_context():
        assert Member.query.count() == 1


def test_invalid_email_and_phone_show_errors(client, app):
    response = register(client, email="not-an-email", phone="12ab")

    assert b"valid email" in response.data
    assert b"valid phone number" in response.data
    with app.app_context():
        assert Member.query.count() == 0


def test_member_codes_increment(client, app):
    register(client)
    register(client, full_name="Rahul Menon", email="rahul@example.com", phone="+91 90000 00000")

    with app.app_context():
        codes = [member.member_code for member in Member.query.order_by(Member.id)]
        assert codes == ["MEM-0001", "MEM-0002"]


def test_search_and_status_filters(client, app):
    register(client)
    register(client, full_name="Rahul Menon", email="rahul@example.com", phone="+91 90000 00000")

    with app.app_context():
        rahul = Member.query.filter_by(email="rahul@example.com").one()
        rahul.status = "Inactive"
        db.session.commit()

    search_html = client.get("/members/?q=rahul").get_data(as_text=True)
    assert "Rahul Menon" in search_html
    assert "Asha Rao" not in search_html

    inactive_html = client.get("/members/?status=Inactive").get_data(as_text=True)
    assert "Rahul Menon" in inactive_html
    assert "Asha Rao" not in inactive_html


def test_edit_member_updates_details(client, app):
    register(client)
    with app.app_context():
        member_id = Member.query.one().id

    response = client.post(
        f"/members/{member_id}/edit",
        data=member_payload(full_name="Asha R. Rao", membership_type="Faculty"),
        follow_redirects=True,
    )

    assert response.status_code == 200
    with app.app_context():
        member = db.session.get(Member, member_id)
        assert member.full_name == "Asha R. Rao"
        assert member.membership_type == "Faculty"
        assert member.member_code == "MEM-0001"


def test_edit_rejects_another_members_email(client, app):
    register(client)
    register(client, full_name="Rahul Menon", email="rahul@example.com", phone="+91 90000 00000")

    with app.app_context():
        rahul_id = Member.query.filter_by(email="rahul@example.com").one().id

    response = client.post(
        f"/members/{rahul_id}/edit",
        data=member_payload(
            full_name="Rahul Menon", email="asha.rao@example.com", phone="+91 90000 00000"
        ),
    )
    assert b"already registered" in response.data


def test_toggle_member_status(client, app):
    register(client)
    with app.app_context():
        member_id = Member.query.one().id

    client.post(f"/members/{member_id}/toggle-status", follow_redirects=True)
    with app.app_context():
        assert db.session.get(Member, member_id).status == "Inactive"

    client.post(f"/members/{member_id}/toggle-status", follow_redirects=True)
    with app.app_context():
        assert db.session.get(Member, member_id).status == "Active"


def test_unknown_member_returns_404(client):
    assert client.get("/members/999").status_code == 404
    assert client.get("/members/999/edit").status_code == 404
