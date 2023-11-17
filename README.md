# homework
This is a dummy python web application used for interviewing.

## Installation
- Install and configure a mysql 8.0 database server and create a mysql user for the application
- Install python3, python3-pip and libmysqlclient-dev via the system package manager
- Install the python package dependencies declared in requirements.txt via pip
- Create the .env configuration file in the top level of the repository with the appropriate values for your mysql database
- Execute the countapp/init_database.py script to create the database structure

## Configuration
Here is an example .env configuration file
```
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=changeme
DB_DATABASE=counter
```

### Running the app
Execute the following command in the top level directory
```
gunicorn --bind 0.0.0.0:6000 --chdir countapp countapp.wsgi:app --reload --timeout=900
```
