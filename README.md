[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/DESIFpxz)
# CS_2025_project

#Link
(https://cs-project-2025-alex-ust-production.up.railway.app)

## Description
Simple reminders/tasks board: add items, filter by type/tag/search, mark done, and keep an optional Telegram chat id with each item

## Setup

```bash
pip3 install -r requirements.txt
docker build -t sever:latest .
docker run --rm -p 8080:8080 -v ${PWD}:/app server
```

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
- **Item**: id, type (reminder/task), title, details, tags, telegramChatId, datetime (reminders), deadline (tasks), completed, created_at, updated_at
- **Tag**: name, created_at
- **Reminder**: id, item_id, telegram_chat_id, scheduled_time (optional), sent, created_at

### Endpoints
- **Items**: `GET /api/items` (filters: type, tag, search, completed); `GET /api/items/<id>`; `POST /api/items`; `PUT /api/items/<id>`; `DELETE /api/items/<id>`; `POST /api/items/<id>/toggle-complete`
- **Tags**: `GET /api/tags`; `GET /api/tags/<tag_name>`; `GET /api/tags/<tag_name>/items`
- **Reminders**: `GET /api/reminders` (filters: item_id, sent); `GET /api/reminders/<id>`; `POST /api/reminders` (itemId, telegramChatId; scheduledTime optional); `PUT /api/reminders/<id>`; `DELETE /api/reminders/<id>`



## Features

- Create reminders or tasks, filter by type/tag/search, and mark completion
- Store optional Telegram chat id with each item for future notifications

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


