# SmartDesk Backend — Local Setup Guide

## 1. Enter Backend Folder

```bash
cd backend
```

---

## 2. Create Virtual Environment

Linux/macOS:

```bash
python3 -m venv venv
```

Windows:

```bash
python -m venv venv
```

---

## 3. Activate Virtual Environment

Linux/macOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` does not exist:

```bash
pip freeze > requirements.txt
```

---

## 5. Run Backend

```bash
uvicorn app.main:app --reload
```

---

## 6. Backend URLs

API:

```txt
http://127.0.0.1:8000
```

Swagger Docs:

```txt
http://127.0.0.1:8000/docs
```

---

## 7. Database

Current database:

```txt
SQLite
```

Database file:

```txt
smartdesk.db
```

---

## 8. Stop Server

Press:

```txt
CTRL + C
```

---

## 9. Recommended Structure

```txt
backend/
│
├── app/
├── venv/
├── requirements.txt
├── smartdesk.db
└── main.py
```
