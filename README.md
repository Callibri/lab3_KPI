# Лабораторна робота 3. CQS

![tests](https://github.com/Callibri/lab3_KPI/actions/workflows/tests.yml/badge.svg)

Рефакторинг лабораторної 2: операції запису оформлені як команди з обробниками, операції читання як запити з обробниками та моделями читання.

## Встановлення

Потрібен Python 3.11 або новіший.

Windows (PowerShell):

```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Linux / macOS:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Запуск

```
uvicorn boxoffice.main:app --app-dir src --reload
```

Документація в браузері: http://127.0.0.1:8000/docs.

Зміна поведінки API порівняно з лабораторною 2: команди не повертають дані. `POST` повертає тільки `{"id": ...}`, `PUT` і `DELETE` повертають 204. Дані отримують запитами `GET`.

## Тести

```
pytest -v
```

- `tests/application` тести команд на in-memory репозиторіях, без бази даних;
- `tests/integration` тести запитів і команд через HTTP з базою даних;
- `tests/domain` тести домену;
- `tests/test_architecture.py` перевірка залежностей між шарами.

## Структура

```
src/boxoffice/
  domain/
  application/
    commands/     команди й їхні обробники
    queries/      запити, обробники, моделі читання, порти читання
    registry.py
  infrastructure/
    repositories.py        запис
    read_repositories.py   читання напряму з бази
  presentation/   контролери: перетворюють HTTP-запит на команду або запит
  bootstrap.py
```

## Документи

- `docs/analysis/lab3.md` порівняльний аналіз;
