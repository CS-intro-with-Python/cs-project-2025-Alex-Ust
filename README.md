[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/DESIFpxz)
# CS_2025_project

# Link
https://cs-project-2025-alex-ust-production.up.railway.app

## Description
Simple reminders/tasks board: add reminders/tasks, edit and delete them.

## Stack
- Flask + SQLAlchemy
- PostgreSQL (Docker Compose)
- HTML + Bootstrap


## Setup (Docker Compose)

```bash
docker compose up --build
```

## Delete docker container
```bash
docker compose down -v
```

The app will be running at `http://localhost:8080`

## Makefile shortcuts

```bash
make install           # install Python deps
make run               # run server (requires DATABASE_URL)
make client            # run client script
make test              # run unit + integration tests
make test-unit         # run unit tests
make test-integration  # run integration tests
make docker-up         # start Docker Compose
make docker-down       # stop Docker Compose and remove volumes
```

## Local Run (without Docker)

1) Install deps:
```bash
pip install -r requirements.txt
```

2) Set DB connection:
```bash
export DATABASE_URL="postgresql://postgres:mysecretpassword@localhost:5432/items_storage"
```

3) Start server:
```bash
python3 server.py
```

4) Start client:
```bash
python3 client.py
```

5) Make testing:
```bash
pytest -s unit_testing.py
pytest -s integration_testing.py
```

## Health

`GET /health` returns `{"status":"ok"}` when the app is up.

## Requirements

Backend:
- Flask
- Python 3.11
- psycopg2-binary (driver for SQLAlchemy)

Testing:
- pytest
- requests
- postman (optional manual testing)

Frontend:
- HTML

## API Structure

### Entity Classes (set at models.py)
- **Task**: id, title, details, deadline, completed, created_at, updated_at
- **Reminder**: id, title, details, scheduled_at, sent, created_at, updated_at

### Endpoints
- **Tasks (API)**:  
`GET /api/tasks`;  
`GET /api/tasks/<task_id>`;  
`POST /api/tasks`;  
`PUT /api/tasks/<task_id>`;  
`DELETE /api/tasks/<task_id>`;  
`POST /api/tasks/<task_id>/if-complete`  

- **Tasks (Actions)**:  
`POST /tasks/create`;  
`GET /tasks/<task_id>/edit`;  
`POST /tasks/<task_id>/update`;  
`POST /tasks/<task_id>/delete`;  
`POST /tasks/<task_id>/if-complete`  

- **Reminders (API)**:  
`GET /api/reminders`;  
`GET /api/reminders/<reminder_id>`;  
`POST /api/reminders`;  
`PUT /api/reminders/<reminder_id>`;  
`DELETE /api/reminders/<reminder_id>`;  
`POST /api/reminders/<reminder_id>/if-complete`  

- **Reminders (Actions)**:  
`POST /reminders/create`;  
`GET /reminders/<reminder_id>/edit`;  
`POST /reminders/<reminder_id>/update`;  
`POST /reminders/<reminder_id>/delete`;  
`POST /reminders/<reminder_id>/if-complete`  

- **Health**:  
`GET /health`



## Features

- Create reminders or tasks
- Remove reminders and tasks 
- Edit reminders and tasks 
- Mark them as done 
- Sort by the type of an item

## Tests

Run unit tests:
```bash
pytest unit_testing.py
```

Run integration tests (Docker must be running):
```bash
docker compose up --build
pytest integration_testing.py
```

Simple API check script:
```bash
python3 client.py
```

## Environment Variables

- `DATABASE_URL`: SQLAlchemy connection string.

## Git

aAl files are placed at the dranch "main"

## Success Criteria

Describe the criteria by which the success of the project can be determined
(this will be updated in the future)

* Criteria 1
Reminders and tasks can be created 

* Criteria 2
Reminders and tasks can be edit 

* Criteria 3
Reminders and tasks can be marked as done

* Criteria 4
Reminders and tasks can be deleted

* Criteria 5
Reminders and tasks can be sorted by their type
