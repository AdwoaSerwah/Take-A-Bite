#!/bin/bash

# Commands to create categories
commands=(
  'create Category name="Lunches"'
  'create Category name="Breakfasts"'
  'create Category name="Desserts"'
  'create Category name="Beverages"'
)

# Loop through each command and execute it
for cmd in "${commands[@]}"; do
  echo $cmd | HBNB_MYSQL_USER=AdwoaSK HBNB_MYSQL_PWD=1m@ALXSCHOOL. HBNB_MYSQL_HOST=AdwoaSK.mysql.pythonanywhere-services.com HBNB_MYSQL_DB=take_a_bite_db HBNB_TYPE_STORAGE=db /home/AdwoaSK/Take-A-Bite/venv/bin/python ./console.py
done
