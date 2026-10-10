import pytest

from app.diary import Diary, DiaryError


def test_average_is_calculated_correctly():
    d = Diary()
    for g in (5, 4, 3):
        d.add_grade("Айдар", "DevOps", g)
    assert d.subject_average("Айдар", "DevOps") == 4.0
    assert d.student_average("Айдар") == 4.0


def test_average_across_subjects():
    d = Diary()
    d.add_grade("Айдар", "DevOps", 5)
    d.add_grade("Айдар", "Базы данных", 4)
    assert d.student_average("Айдар") == 4.5


@pytest.mark.parametrize("bad", [0, 6, -1, "5", 3.5])
def test_invalid_grade_is_rejected(bad):
    with pytest.raises(DiaryError):
        Diary().add_grade("Айдар", "DevOps", bad)


def test_empty_name_is_rejected():
    with pytest.raises(DiaryError):
        Diary().add_grade("  ", "DevOps", 5)


def test_unknown_student_has_zero_average():
    assert Diary().student_average("Никто") == 0.0
