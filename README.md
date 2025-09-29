# Blog API (Django REST)

API לבניית בלוג עם משתמשים, כתבות ותגובות.

## התקנה מהירה
```bash
python -m venv .venv && source .venv/bin/activate  # ב-Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser  # ליצירת מנהל (is_staff)
python manage.py runserver
```

## מסדי נתונים
ברירת מחדל: sqlite. לשימוש ב-PostgreSQL ערוך `.env`:
```
DB_ENGINE=postgres
POSTGRES_DB=blog
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

## נקודות קצה עיקריות
- POST `/api/register/` — יצירת משתמש חדש
- POST `/api/token/` — קבלת JWT (username+password)
- POST `/api/token/refresh/` — חידוש טוקן
- GET `/api/articles/` — רשימת כתבות, חיפוש: `?search=<query>`
- GET `/api/articles/<id>/` — צפייה בכתבה
- POST `/api/articles/` — יצירה (מנהל בלבד, דורש שדה raw_tags אופציונלי)
- PUT `/api/articles/<id>/` — עדכון (מנהל בלבד)
- DELETE `/api/articles/<id>/` — מחיקה (מנהל בלבד)
- GET `/api/articles/<id>/comments/` — תגובות לכתבה
- POST `/api/articles/<id>/comments/` — הוספת תגובה (מחובר)
- DELETE `/api/comments/<id>/` — מחיקת תגובה (מנהל בלבד)

## הערות איכות קוד
- בלי `print`, בלי קוד מת, קבצים קצרים (<~200 שורות).
- שימוש ב-`.env` לסודות והגדרות.
- CORS נשלט ב-`CORS_ALLOWED_ORIGINS`.
- DRF SearchFilter מאפשר חיפוש לפי כותרת/תוכן/תגים/שם כותב.
