@echo off
title Django Server (Port 80)
echo Starting Django Server at http://localhost:80 ...
venv\Scripts\python manage.py runserver 0.0.0.0:80
pause
