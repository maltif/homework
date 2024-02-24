# homework
This is a simple python web application for testing/demo.

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

## Dockerization Guide

### 1. Clone the Repository and Create a New Branch

Clone the repository containing your Python web application code and navigate into the project directory. Then, create a new branch for working on dockerization:

```bash
git clone https://github.com/ustream/homework.git
cd homework
git checkout -b dockerize-webapp
```

### 2. Dockerfile
Create a `Dockerfile` in the project directory with the following content:

```Dockerfile
# Use an official Python runtime as the base image
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    default-mysql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for MySQL client library
ENV MYSQLCLIENT_CFLAGS="-I/usr/include/mysql"
ENV MYSQLCLIENT_LDFLAGS="-L/usr/lib/x86_64-linux-gnu -lmysqlclient"

# Set environment variables
ENV FLASK_APP=countapp.app
ENV FLASK_RUN_HOST=0.0.0.0

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port
EXPOSE 6060

# Run the Flask application
CMD ["gunicorn", "--bind", "0.0.0.0:6000", "--chdir", "countapp", "wsgi:app", "--reload", "--timeout=900"]

```

### 3. .env Configuration

Create a `.env` file in the top level of the repository with the appropriate values for your MySQL database:

```dotenv
DB_HOST=mysql
DB_PORT=3306
DB_USER=root
DB_PASSWORD=changeme
DB_DATABASE=counter
```

### 4. add Werkzeug==2.2.2 package to requirements.txt

Ensure the Werkzeug==2.2.2 package is included in the requirements.txt file to avoid errors in the web application.

```
flask==2.2.3
sqlalchemy==2.0.5.post1
sqlalchemy-utils==0.40.0
flask-mysqldb==1.0.1
pymysql==1.0.2
python-decouple==3.8
gunicorn==20.1.0
cryptography==40.0.2
Werkzeug==2.2.2
```

### 5. Docker Compose (Optional)

You can also use Docker Compose to manage both containers. Create a `docker-compose.yml` file in the project directory:

```yaml
version: '3'
services:
  web:
    build: .
    container_name: web
    ports:
      - "6060:6000"
    environment:
      - MYSQL_HOST=mysql
      - MYSQL_USER=root
      - MYSQL_PASSWORD=changeme
      - MYSQL_DATABASE=counter
      - MYSQL_PORT=3306
    depends_on:
      - mysql
  mysql:
    image: mysql:8.0
    container_name: mysql
    environment:
      - MYSQL_ROOT_PASSWORD=changeme
      - MYSQL_DATABASE=counter
```

### 6. Build and Run

Build and run the Docker containers in detach mode using the following command:

```bash
docker-compose up -d --build
```

### 7. Run the `init_database` Script to Create the Database Structure

- **Log in to the web container and run `init_database.py` to create the database schema:**

  To access the web container's shell, execute the following command:

  ```bash
  docker exec -it web /bin/bash
  ```

- **Execute the `init_database.py` script:**
  
  Once logged into the web container, run the following command to execute the `init_database.py` script:

  ```bash
  python3 countapp/init_database.py
  ```

- **Access the Web Application:**

  After initializing the database structure, you can access the web application via your favorite web browser. Use the following URL:

  [http://localhost:6060](http://localhost:6060)

  > **Note:** We've exposed the web application on port 6060 to avoid conflicts with blocked ports, such as 6000, which may be restricted by certain web browsers. By exposing the application on port 6060, we ensure smooth accessibility without encountering port-related issues.


### 8. Logging / Troubleshooting

If something goes wrong during the build or run steps, you can troubleshoot using the following commands:

- **Docker Build Logs:**
  ```bash
  docker-compose logs --tail="all" web
  ```
  This command displays the logs generated during the Docker build process for the web container. It can help identify any errors or warnings that occurred during the build.

- **Docker Container Logs:**
  ```bash
  docker-compose logs --tail="all" web
  ```
  This command displays the logs generated by the running web container. It can provide information about any runtime errors or issues encountered by the application.

- **Check Docker Container Status:**
  ```bash
  docker-compose ps
  ```
  This command displays the status of all containers managed by Docker Compose. It can help determine if any containers have stopped unexpectedly.

- **Inspect Docker Container:**
  ```bash
  docker-compose exec web /bin/bash
  ```
  This command allows you to access the shell of the running web container. From there, you can manually inspect files, configurations, or execute commands to diagnose issues.

- **Check Docker Network:**
  ```bash
  docker network inspect <network_name>
  ```
  Replace `<network_name>` with the name of the Docker network used by your containers. This command provides detailed information about the Docker network, including container IP addresses and connectivity.

- **Verify Container Port Binding:**
  ```bash
  docker-compose port web 6000
  ```
  This command verifies that the web container is correctly binding to port 6000 on the host machine. It can help identify port binding issues if the application is not accessible.

- **Check Container Resource Usage:**
  ```bash
  docker stats web
  ```
  This command displays real-time resource usage statistics for the web container, including CPU, memory, and network usage. It can help identify performance bottlenecks or resource constraints.
