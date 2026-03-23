# Flask Users API

A simple REST API built with Flask that implements a full CRUD system using PostgreSQL.

## Features

- Create users (POST)
- Get all users (GET)
- Get user by ID (GET)
- Update users (PUT)
- Delete users (DELETE)


## Endpoints


GET    | /users          Get all users           
GET    | /users/<id>     Get user by ID          
POST   | /users          Create a new user       
PUT    | /users/<id>     Update user             
DELETE | /users/<id>     Delete user             


## Tech Stack

- Python
- Flask
- PostgreSQL
- SQLAlchemy

---

## Run locally

```bash
pip install -r requirements.txt
python3 app.py