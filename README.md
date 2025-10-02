# PTCMAKET

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)

This repository is for internship project.

## Requirements
- Python
- Django
- Django REST Framework
- Django Filter



### How to Run
1. Clone the repository
2. Create and activate a virtual environment:
   ```
   pip install pipenv
   pipenv shell
   ```
3. Install dependencies:
   ```
   pipenv install
   ```
4. Run migrations:
   ```
   python manage.py migrate
   ```
5. Create a superuser (optional for admin access):
   ```
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```
    python manage.py runserver
   ```

### Environment Variables
Configure in `.env` file:

-   check .env.example for details
```
DJANGO_PRODUCTION_SECRET_KEY=
DJANGO_ALLOWED_HOSTS=
DATABASE_URL=
DJANGO_CORS_ALLOWED_ORIGINS=
```
