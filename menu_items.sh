#!/bin/bash

# Array of commands to create multiple menu items
commands=(
  'create MenuItem name="Grilled Chicken" description="Juicy grilled chicken served with a side of vegetables." price=20.00 category_id="0165c896-e8ed-4b54-aabb-da1720854e8a" image_url="images/fresh-grill-bbq-chicken.jpg"'
  'create MenuItem name="Vegan Salad" description="A fresh mix of greens, avocado, tomatoes, and nuts." price=10.00 category_id="0165c896-e8ed-4b54-aabb-da1720854e8a" image_url="images/fresh-salade-wooden-background.jpg"'
  'create MenuItem name="Beef Burger" description="Classic beef burger with lettuce, tomato, and cheese." price=25.00 category_id="0165c896-e8ed-4b54-aabb-da1720854e8a" image_url="images/burger2.jpg"'
  'create MenuItem name="Spaghetti Bolognese" description="Spaghetti served with rich bolognese sauce and parmesan." price=32.00 category_id="0165c896-e8ed-4b54-aabb-da1720854e8a" image_url="images/ai-generated-8725190_1280.png"'
  'create MenuItem name="Fried Rice" description="Rice stir-fried with vegetables, hot green pepper and fried prawns." price=20.00 category_id="0165c896-e8ed-4b54-aabb-da1720854e8a" image_url="images/fried-rice.jpg"'
  'create MenuItem name="Jollof Rice" description="Spicy jollof rice served with chicken kebab or grilled fish." price=25.00 category_id="0165c896-e8ed-4b54-aabb-da1720854e8a" image_url="images/jollof.jpg"'
  'create MenuItem name="Chocolate Brownie" description="Rich brownie with vanilla ice cream and strawberries." price=15.00 category_id="7d136cbb-7d54-41a9-8142-a4fccb0d7f83" image_url="images/chocolate-brownie.jpg"'
  'create MenuItem name="Strawberry Milkshake" description="Refreshing milkshake made with fresh strawberries." price=12.00 category_id="96cf12ba-6dcf-43cd-bd60-5c626ec2be1f" image_url="images/strawberry-milkshake.jpg"'
  'create MenuItem name="Pancakes" description="Delicious pancakes served with ice cream and chocolate syrup." price=20.00 category_id="020edfb8-6581-4ea3-8f93-009e4aea8663" image_url="images/pancake.jpg"'
  'create MenuItem name="Waffles" description="Belgian waffles with vanilla ice cream and strawberries." price=20.00 category_id="020edfb8-6581-4ea3-8f93-009e4aea8663" image_url="images/waffle.jpg"'
  'create MenuItem name="Fish and Chips" description="Succulent fried fish served with fries and a slice of lemon." price=22.00 category_id="0165c896-e8ed-4b54-aabb-da1720854e8a" image_url="images/fish-chips.jpg"'
  'create MenuItem name="Doughnut" description="A light and fluffy doughnut covered in sweet icing." price=15.00 category_id="7d136cbb-7d54-41a9-8142-a4fccb0d7f83" image_url="images/donut.jpg"'
  'create MenuItem name="Orange Juice" description="Freshly squeezed orange juice bursting with zesty flavour." price=10.00 category_id="96cf12ba-6dcf-43cd-bd60-5c626ec2be1f" image_url="images/orange-juice.jpg"'
  'create MenuItem name="Fruit Salad" description="Fresh and healthy mix of seasonal fruits." price=15.00 category_id="7d136cbb-7d54-41a9-8142-a4fccb0d7f83" image_url="images/fruit-salad.jpg"'
  'create MenuItem name="Coffee" description="Hot brewed coffee with a rich aroma and cookie." price=8.00 category_id="96cf12ba-6dcf-43cd-bd60-5c626ec2be1f" image_url="images/coffee.jpg"'
  'create MenuItem name="Mango Juice" description="Refreshing juice made with ripe mangoes." price=8.00 category_id="96cf12ba-6dcf-43cd-bd60-5c626ec2be1f" image_url="images/mango-juice.jpg"'
)

# Loop through each command and execute it
for cmd in "${commands[@]}"; do
  echo $cmd | HBNB_MYSQL_USER=root HBNB_MYSQL_PWD=12345678 HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=take_a_bite_db HBNB_TYPE_STORAGE=db ./console.py
done
