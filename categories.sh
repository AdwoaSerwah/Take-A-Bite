#!/bin/bash

# Commands to create categories
commands=(
  'create Category name="Breakfast"'
  'create Category name="Lunch"'
  'create Category name="Desserts"'
  'create Category name="Beverages"'
)

# Loop through each command and execute it
for cmd in "${commands[@]}"; do
  echo $cmd | HBNB_MYSQL_USER=root HBNB_MYSQL_PWD=12345678 HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=take_a_bite_db HBNB_TYPE_STORAGE=db ./console.py
done
