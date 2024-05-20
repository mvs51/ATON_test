# Test task for internship in ATON
# Currency rates parser

This service is for collecting and managing currecy rates.

## Requirements
Django 4.2.13
djangorestframework 3.15.1
sqlparse 0.5.0
pandas 2.2.2
seaborn 0.13.2

## Setup
- Create and activate virtual environment
- Install requirements from requirements.txt
```
pip install -r requirements.txt
``` 
- Apply migrations:
```
python3 manage.py migrate
```
- Run custom manage command to setup initial baselines:
```
python3 manage.py set_baselines
```
- Launch project with:
```
python3 manage.py runserver
```