"""Бизнес-логика «Электронного дневника»: оценки студентов по предметам."""

MIN_GRADE = 1
MAX_GRADE = 5


class DiaryError(ValueError):
    """Ошибка валидации данных дневника."""


class Diary:
    def __init__(self):
        # {имя студента: {предмет: [оценки]}}
        self._data = {}

    def add_grade(self, student, subject, grade):
        student, subject = student.strip(), subject.strip()
        if not student or not subject:
            raise DiaryError("Имя студента и предмет не могут быть пустыми")
        if not isinstance(grade, int) or not MIN_GRADE <= grade <= MAX_GRADE:
            raise DiaryError(f"Оценка должна быть целым числом от {MIN_GRADE} до {MAX_GRADE}")
        self._data.setdefault(student, {}).setdefault(subject, []).append(grade)

    def students(self):
        return sorted(self._data)

    def grades(self, student):
        return {s: list(g) for s, g in self._data.get(student, {}).items()}

    def subject_average(self, student, subject):
        marks = self._data.get(student, {}).get(subject, [])
        return round(sum(marks) / len(marks), 2) if marks else 0.0

    def student_average(self, student):
        marks = [m for g in self._data.get(student, {}).values() for m in g]
        return round(sum(marks) / len(marks), 2) if marks else 0.0
