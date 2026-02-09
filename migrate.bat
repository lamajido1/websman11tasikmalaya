@echo off
echo Running Migrations...
venv\Scripts\python manage.py makemigrations
venv\Scripts\python manage.py migrate
pause
