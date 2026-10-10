import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_main_page_opens(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "Электронный дневник" in r.get_data(as_text=True)


def test_add_grade_and_get_student(client):
    r = client.post("/grades", data={"student": "Айдар", "subject": "DevOps", "grade": "5"})
    assert r.status_code == 302
    data = client.get("/api/students/Айдар").get_json()
    assert data["average"] == 5.0


def test_invalid_grade_returns_400(client):
    r = client.post("/grades", data={"student": "Айдар", "subject": "DevOps", "grade": "9"})
    assert r.status_code == 400


def test_unknown_student_returns_404(client):
    assert client.get("/api/students/Нет").status_code == 404


def test_health(client):
    assert client.get("/health").get_json() == {"status": "ok"}


def test_student_is_shown_on_page_after_adding(client):
    client.post("/grades", data={"student": "Айдар", "subject": "DevOps", "grade": "5"})
    html = client.get("/").get_data(as_text=True)
    assert "Айдар" in html and "DevOps" in html and "5.00" in html


def test_error_message_is_shown_for_missing_grade(client):
    r = client.post("/grades", data={"student": "Айдар", "subject": "DevOps"})
    assert r.status_code == 400
    assert "Выберите оценку" in r.get_data(as_text=True)


def test_css_is_served(client):
    assert client.get("/static/style.css").status_code == 200
