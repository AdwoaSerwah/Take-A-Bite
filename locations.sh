#!/bin/bash

# Commands to create locations with arbitrary delivery prices between 5 and 20 Ghana cedis
commands=(
  'create Location name="Pickup" delivery_price=0.00'
  'create Location name="Ashongman Estate" delivery_price=0.00'
  'create Location name="Haatso" delivery_price=5.00'
  'create Location name="West Legon" delivery_price=6.50'
  'create Location name="Madina" delivery_price=8.00'
  'create Location name="Adenta" delivery_price=10.50'
  'create Location name="Ashaley Botwe" delivery_price=12.00'
  'create Location name="North Legon" delivery_price=13.50'
  'create Location name="Agbogba" delivery_price=7.50'
  'create Location name="Dome" delivery_price=4.00'
  'create Location name="Kwabenya" delivery_price=2.00'
  'create Location name="Achimota" delivery_price=10.00'
  'create Location name="Pokuase" delivery_price=6.00'
  'create Location name="Ofankor" delivery_price=14.00'
  'create Location name="Abokobi" delivery_price=5.50'
  'create Location name="Pantang" delivery_price=14.00'
)

# Loop through each command and execute it
for cmd in "${commands[@]}"; do
  echo $cmd | HBNB_MYSQL_USER=your_username HBNB_MYSQL_PWD=your_password HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=take_a_bite_db HBNB_TYPE_STORAGE=db ./console.py
done
