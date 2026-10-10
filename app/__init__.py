from flask import Flask, jsonify, redirect, render_template, request, url_for

from .diary import Diary, DiaryError


def create_app():
    app = Flask(__name__)
    diary = Diary()
    app.config["DIARY"] = diary

    @app.get("/")
    def index():
        rows = [(s, diary.student_average(s)) for s in diary.students()]
        return render_template("index.html", rows=rows)

    @app.post("/grades")
    def add_grade():
        try:
            diary.add_grade(
                request.form.get("student", ""),
                request.form.get("subject", ""),
                int(request.form.get("grade", "")),
            )
        except (DiaryError, ValueError) as exc:
            return render_template("index.html", rows=[], error=str(exc)), 400
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
