[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/DESIFpxz)
# CS_2025_project

#Link
(https://cs-project-2025-alex-ust-production.up.railway.app)

## Description
Simple reminders/tasks board: add items, filter by type, mark done


## Setup (Docker Compose)

```bash
docker compose up --build
```

The app will be running at `http://localhost:8080`

## Requirements

Backend:
- Flask 
- Python 3.11 

Testing:
- requests
- postman (for server endpoints testing)

Frontend:
- HTML

## API Structure

### Entity Classes (models.py)
- **Item**: id, type (reminder/task), title, details, datetime (reminders), deadline (tasks), completed, created_at, updated_at
- **Reminder**: id, item_id, scheduled_time (optional), sent, created_at

### Endpoints
- **Tasks**: `GET /api/tasks` (filters: completed); `GET /api/tasks/<id>`; `POST /api/tasks`; `PUT /api/tasks/<id>`; `DELETE /api/tasks/<id>`; `POST /api/tasks/<id>/toggle-complete`
- **Reminders**: `GET /api/reminders` (filters: item_id, sent); `GET /api/reminders/<id>`; `POST /api/reminders` (scheduledTime optional); `PUT /api/reminders/<id>`; `DELETE /api/reminders/<id>`



## Features

- Create reminders or tasks
- Remove reminders and tasks 
- Edit reminders and tasks 

## Git

main
Specify which branch will store the latest stable version of the application

## Success Criteria

Describe the criteria by which the success of the project can be determined
(this will be updated in the future)

* Criteria 1
Reminders and tasks can be created 

* Criteria 2
Reminders and tasks can be edit
