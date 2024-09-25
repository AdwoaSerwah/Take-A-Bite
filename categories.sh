#!/bin/bash

# Commands to create categories
commands=(
  'create Category name="Breakfasts"'
  'create Category name="Lunches"'
  'create Category name="Desserts"'
  'create Category name="Beverages"'
)

# Loop through each command and execute it
for cmd in "${commands[@]}"; do
  echo $cmd | HBNB_MYSQL_USER=your_username HBNB_MYSQL_PWD=your_password HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=take_a_bite_db HBNB_TYPE_STORAGE=db ./console.py
done
