# Take-A-Bite

Take-A-Bite is a web application designed to help users easily browse and order food from a variety of restaurants. The project was built as a portfolio piece for Holberton School and aimed at learning full-stack web development using technologies like Python (Flask), JavaScript, SQLAlchemy, and jQuery.

## Introduction

This project is deployed [here](https://adwoask.pythonanywhere.com/), and you can read the blog post about the project [here](https://medium.com/@lindseylinwood56/take-a-bite-revolutionizing-food-delivery-in-accra-62bf3848529f).

**Project timeline:** August 2, 2024 – September 24, 2024  
**Author:** [Adwoa Serwah](https://www.linkedin.com/in/adwoa-kyei-baffour-892490192)

Take-A-Bite was created with the goal of simplifying the online food ordering experience, particularly for users in Accra, Ghana. It provides users with a seamless way to select food, customize their order, and complete payments. 

I worked on both the backend and frontend, focusing on delivering a robust and user-friendly experience. My role involved:
- Building and managing database models using SQLAlchemy
- Developing Flask routes for data handling and payment processing
- Creating dynamic and responsive frontend pages using HTML5, CSS3, and JavaScript (with jQuery).

## Installation

### Prerequisites
- Python 3.10 installed
- MySQL installed and running
- pip (Python package installer)
- Git (for cloning the repository)

### Installation Instructions


To get a local copy up and running, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AdwoaSerwah/Take-A-Bite.git
   ```

2. **Navigate to the project directory**:

   ```bash
   cd Take-A-Bite
   ```
3. **Create a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**:

   ```
   bash
   pip install -r requirements.txt
   ```

## Database Setup

To set up the MySQL database for the Take-A-Bite project, follow these steps:

1. **Install MySQL**: Make sure you have MySQL installed on your machine. If you haven't installed it yet, refer to the [MySQL Installation Guide](https://dev.mysql.com/doc/refman/8.0/en/installing.html).

2. **Create the database and user** by running the following command in your terminal:

   You can either run the SQL commands directly or use the setup file:

   - **Option 1: Run the SQL commands directly**:

     ```bash
     mysql -u root -p  # Log into MySQL
     ```

     Then execute the following SQL commands:

     ```sql
     CREATE DATABASE IF NOT EXISTS take_a_bite_db;
     CREATE USER IF NOT EXISTS 'your_username'@'localhost' IDENTIFIED BY 'your_password';
     GRANT ALL PRIVILEGES ON `take_a_bite_db`.* TO 'your_username'@'localhost';
     FLUSH PRIVILEGES;
     ```

   - **Option 2: Use the setup file**:

     If you have a `setup_mysql_dev.sql` file, first, open the file in a text editor and modify the default values for the username and password:

     ```sql
     CREATE DATABASE IF NOT EXISTS take_a_bite_db;
     CREATE USER IF NOT EXISTS 'your_username'@'localhost' IDENTIFIED BY 'your_password';
     GRANT ALL PRIVILEGES ON `take_a_bite_db`.* TO 'your_username'@'localhost';
     FLUSH PRIVILEGES;
     ```

     After making the changes, you can execute the file directly:

     ```bash
     mysql -u root -p < setup_mysql_dev.sql
     ```

     Or, if you need to use sudo:

     ```bash
     sudo mysql < setup_mysql_dev.sql
     ```

### Database Population

To populate the database with initial data, follow these steps:

1. **Run the Categories Script**:
   Open `categories.sh` and replace the placeholders (`your_username`, `your_password`) with your actual MySQL credentials. Then run the script:

   ```bash
   chmod +x categories.sh
   ./categories.sh

2. **Update the Menu Items Script**:
   Similarly, open menu_items.sh and replace the placeholders with your actual credentials. Before running the script, also replace the category ID placeholders (example, CATEGORY_ID_BREAKFAST) with the actual IDs created in the previous step.

3. **Run the Menu Items Script**:
   After updating the menu_items.sh, run the script:

   ```bash
   chmod +x menu_items.sh
   ./menu_items.sh
   ```

4. **Run the Locations Script**:
   Finally, open locations.sh, update it with your credentials, and run it:

   ```bash
   chmod +x locations.sh
   ./locations.sh
   ```

Notes
Make sure to replace your_username, your_password, and other placeholders with the actual details you created during the setup process.

Bash Environment: These instructions assume you are using a Unix-like environment (Linux, macOS, etc.) where bash is available. If you're on Windows, you may need to use Git Bash or Windows Subsystem for Linux (WSL).


## Environment Variables

**Create a `.env` file in the root directory of your project and populate it with the following variables**:

```plaintext
HBNB_ENV=dev
HBNB_MYSQL_USER=your_username_here
HBNB_MYSQL_PWD=your_password_here
HBNB_MYSQL_HOST=localhost
HBNB_MYSQL_DB=take_a_bite_db
HBNB_TYPE_STORAGE=db
DATABASE_URL=mysql+mysqldb://your_username_here:your_password_here@localhost/take_a_bite_db
HBNB_API_HOST=0.0.0.0
HBNB_API_PORT=5005

SECRET_KEY=your_secret_key_here

MAIL_USERNAME=your_email
MAIL_PASSWORD=your_password
MAIL_DEFAULT_SENDER=your_default_email

PAYSTACK_SECRET_KEY=your_paystack_secret_key
```

**Generate the SECRET_KEY**
To generate a random secret key for your application, run the following command:

```bash
python secret_key.py
```
This will output a secret key that you should copy and paste into your .env file as the value for SECRET_KEY.

**Email Configuration**
Gmail’s SMTP server is what is being used.

Note: If you have two-step verification enabled for your Google account, you will need to generate an App Password to use as the MAIL_PASSWORD.

**Obtain Paystack API Keys**
1. Go to the Paystack website and sign up for an account if you
don't have one. Follow the instructions to obtain your public and secret keys.

2. Replace the placeholder your_paystack_secret_key in the .env file with your actual Paystack secret key.

3. In your static JavaScript file static/scripts/checkout.js, replace the following line with your actual Paystack public key:

```javascript
key: 'pk_test_3172601967078640096a6f10075e6537df112f15',
```

Important: Do not use your Paystack secret key in your client-side code (JavaScript). Only use the public key in the client-side code for security reasons.

Notes
The Paystack public key is safe to use in client-side code. The secret key should remain confidential and only be used in your server-side code (e.g., in API calls to Paystack).

### Run the Application:
Start your application using:
```bash
python3 -m api.v1.app
```

This will start the Flask application, and you can access it in your browser at http://127.0.0.1:5005.

## Usage
- Users can browse available food options, view their cart, and place an order.

- Payment processing is integrated using the Paystack API for card and mobile payments.

- The app is responsive, ensuring a good experience across devices.

## Features
1. **Food Browsing**: Users can view food items, add them to the cart, and customize their order.

2. **Payment Integration**: Payments are processed using Paystack, supporting card and mobile money transactions.

3. **Order Summary**: Users can view a detailed summary of their order, including delivery fees and payment options.

## Contributing
Contributions are welcome! Please follow the standard GitHub flow:

1. Fork the repository

2. Create a feature branch (git checkout -b feature/YourFeature)

3. Commit your changes (git commit -m 'Add YourFeature')

4. Push to the branch (git push origin feature/YourFeature)

5. Create a new Pull Request

## Related Projects

- [Flask](https://flask.palletsprojects.com/): A lightweight WSGI web application framework in Python.

- [Paystack Integration](https://paystack.com/): A platform for accepting payments, which you're using in your project.

- [Holberton School Projects](https://www.holbertonschool.com/): Projects from Holberton School, where this project is being developed.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/AdwoaSerwah/Take-A-Bite/blob/main/LICENSE) file for details.


## Links
- **GitHub Repository**: [Take-A-Bite Repository](https://github.com/AdwoaSerwah/Take-A-Bite)
- **Deployed Project**: [Take-A-Bite](https://adwoask.pythonanywhere.com/) 
- **Project Blog Post**: [Final Blog](https://medium.com/@lindseylinwood56/take-a-bite-revolutionizing-food-delivery-in-accra-62bf3848529f) 
- **LinkedIn**: [Adwoa Serwah](https://www.linkedin.com/in/adwoa-kyei-baffour-892490192)


## Screenshots
![Login Page](screenshots/login.png)

![HomePage](screenshots/home.png)

![Menu Page](screenshots/menu.png)


