# How to use:
*  Install Python3.7
*  Create a Python virtual environment using your favorite venv tool OR just install everything globally
*  `cd app`
*  `pip install` all the requirements listed in `requirements.txt`
*  `python manage.py migrate` to create database with necessary tables
*  `python manage.py runserver` to run locally
*  Open `localhost:8000` in web browser to view homepage. You did it!
*  `python manage.py createsuperuser` to create admin user if you need one
*  Open `localhost:8000/admin` to view admin panel and look at database contents
