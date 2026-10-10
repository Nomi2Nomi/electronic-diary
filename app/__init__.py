from flask import Flask, jsonify, redirect, render_template, request, url_for

from .diary import Diary, DiaryError


def tone(value):
    """Цветовая категория оценки или среднего балла для оформления."""
    if value >= 4.5:
        return "great"
    if value >= 3.5:
        return "good"
    if value >= 2.5:
        return "mid"
    return "low"


def create_app():
    app = Flask(__name__)
    diary = Diary()
    app.config["DIARY"] = diary

    def render_index(status=200, error=None, form=None):
        students = []
        for name in diary.students():
            avg = diary.student_average(name)
            subjects = [
                {
                    "name": subj,
                    "grades": marks,
                    "average": diary.subject_average(name, subj),
                    "tone": tone(diary.subject_average(name, subj)),
                }
                for subj, marks in sorted(diary.grades(name).items())
            ]
            students.append({"name": name, "average": avg, "tone": tone(avg), "subjects": subjects})
        subjects_all = sorted({s["name"] for st in students for s in st["subjects"]})
        page = render_template(
            "index.html",
            students=students,
            subjects_all=subjects_all,
            error=error,
            form=form or {},
            tone=tone,
        )
        return page, status

    @app.get("/")
    def index():
        return render_index()

    @app.post("/grades")
    def add_grade():
        form = {k: request.form.get(k, "") for k in ("student", "subject", "grade")}
        try:
            diary.add_grade(form["student"], form["subject"], int(form["grade"]))
        except DiaryError as exc:
            return render_index(400, str(exc), form)
        except ValueError:
            return render_index(400, "Выберите оценку от 1 до 5", form)
        return redirect(url_for("index"))

    @app.get("/api/students/<name>")
    def student_api(name):
        grades = diary.grades(name)
        if not grades:
            return jsonify(error="Студент не найден"), 404
        return jsonify(student=name, grades=grades, average=diary.student_average(name))

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    return app
