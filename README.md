[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/DESIFpxz)
# CS_2025_project

#Link
(https://cs-project-2025-alex-ust-production.up.railway.app)

## Description
Simple reminders/tasks board: add reminders/tasks, edit and delete them.


## Setup (Docker Compose)

```bash
docker compose up --build
```

The app will be running at `http://localhost:8080`

## Requirements

Backend:
- Flask 
- Python 3.11 
- psycopg2-binary (driver for SQLAlchemy)

Testing:
- requests
- postman (for server endpoints testing)

Frontend:
- HTML

## API Structure

### Entity Classes (models.py)
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



## Features

- Create reminders or tasks
- Remove reminders and tasks 
- Edit reminders and tasks 
- Mark them as done 
- Sort by the type of an item

## Git

main

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
