Project List API
This is a simple Flask API for managing list of projects. It uses SQLAlchemy to interact with a SQLite database.
Setup:
Python 3.11.7

Install the required packages flask, flask_sqlalchemy
`pip install -r requirements.txt`

Run the application:
`python app.py`

The application will be running on http://localhost:5001
http://127.0.0.1:5001/projects

Endpoints
GET /: Returns a list of all projects.
POST /updated: Adds a new project. The request body should be a JSON object with a name field.
GET /projects: Returns a list of all projects in JSON format.
PUT /projects/<id>: Updates the name of the project with the given ID. The request body should be a JSON object with a name field.
DELETE /projects/<id>: Deletes the project with the given ID.

Database
The application uses a SQLite database (projects.db) to store the projects. Each project has an id and a name. The id is an integer
and is automatically generated by the database. The name is a string and must be unique.