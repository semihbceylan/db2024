# db2024
**BLG 317E Database Systems Term Project**

This project is a web application built with Flask for the backend and React for the frontend. It connects to a MySQL Workbench database and displays data from multiple tables.

## Prerequisites

Make sure you have the following installed on your machine:
- Python 3.x
- Node.js and npm
- MySQL Workbench (for managing the database)

## Initial Setup

### 1. Clone the Repository

Clone the repository to your local machine:

```
git clone https://github.com/ceylans20/db2024.git
cd db2024
```
### 2. Setting Up and Running the Flask Server

Copy and paste the commands to a terminal:
```
cd server
pip install -r requirements.txt
notepad .env
```
Change it with your credentials.

FLASK_ENV=development
MYSQL_HOST=localhost
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=your_database_name

```
flask run
```

### 3. Setting Up the Frontend
```
cd ../client
npm install
npm start
```

This should start the React app at http://localhost:3000