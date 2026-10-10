# Электронный дневник

## Описание
Небольшое учебное веб-приложение на Flask с минималистичным интерфейсом (светлая и тёмная темы): добавление оценок студентов (1–5) по предметам и расчёт среднего балла. Создано для СРОП по дисциплине «Прикладные аспекты DevOps» (вариант 23).

## Используемые технологии
Python 3.12, Flask, pytest, Git, GitHub Actions.

## Установка
```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск
```bash
python run.py
```
Приложение: http://127.0.0.1:5000

## Тестирование
```bash
pytest -v
```

## CI/CD
Файл `.github/workflows/ci.yml`. Запускается при каждом `push` и `pull_request`:
1. **Build** — установка зависимостей, компиляция кода, проверка создания приложения.
2. **Test** — запуск `pytest` (выполняется только после успешного Build, `needs: build`).
