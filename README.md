[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/DESIFpxz)
# CS_2025_project

#Link
(https://cs-project-2025-alex-ust-production.up.railway.app)

## Description
Note, reminred and tasks taking app, which allows user to track them by time, sort by some tags and mark their progress. 

## Setup

You can run backend locally using this command:
```bash
flask --app server run -h 0.0.0.0 -p 8080
```

Describe the steps to set up the environment and run the application. This can be a bash script or docker commands.

```bash
pip3 install -r requirements.txt
docker build -t sever:latest .
docker run --rm -p 8080:8080 -v ${PWD}:/app server

```

## Requirements

Describe technologies, libraries, languages you are using (this can be updated in the future).

Backend:
- Flask (web framework)
- Python 3.7+ (uses built-in modules: uuid, datetime, enum)
- requests for telegram bot (?) not decided yet

Testing:
- requests
- postman (for server endpoints testing)

Frontend:
- HTML
- JavaScript (ES6+)

## API Structure

### Entity Classes

The application uses the following entity classes (defined in `models.py`):

1. **Item**: Represents notes, reminders, or tasks
   - Attributes: id, type (note/reminder/task), title, details, tags, datetime, completed, created_at, updated_at
   - Supports all three item types with optional datetime for reminders and tasks

2. **User**: Represents application users who own items and reminders
   - Attributes: id, name, email, telegramChatId, timezone, created_at, updated_at
   - Stores notification preferences such as Telegram chat ID and timezone

3. **Tag**: Represents tags for categorizing items
   - Attributes: name, color (optional), created_at
   - Tags are automatically normalized to lowercase

4. **Reminder**: Represents Telegram reminder notifications
   - Attributes: id, item_id, telegram_chat_id, scheduled_time, sent, created_at
   - Separate from Item type 'reminder' - this represents the actual notification mechanism

### API Endpoints

#### Users
- `GET /api/users` - Get all users (supports query parameter: email)
- `GET /api/users/<user_id>` - Get a specific user by ID
- `POST /api/users` - Create a new user (requires: name; optional: email, telegramChatId, timezone)
- `PUT /api/users/<user_id>` - Update an existing user
- `DELETE /api/users/<user_id>` - Delete a user

#### Items
- `GET /api/items` - Get all items (supports query parameters: type, tag, search, completed)
- `GET /api/items/<item_id>` - Get a specific item by ID
- `POST /api/items` - Create a new item
- `PUT /api/items/<item_id>` - Update an existing item
- `DELETE /api/items/<item_id>` - Delete an item
- `POST /api/items/<item_id>/toggle-complete` - Toggle completion status

#### Tags
- `GET /api/tags` - Get all tags
- `GET /api/tags/<tag_name>` - Get a specific tag by name
- `GET /api/tags/<tag_name>/items` - Get all items with a specific tag

#### Reminders
- `GET /api/reminders` - Get all reminders (supports query parameters: item_id, sent)
- `GET /api/reminders/<reminder_id>` - Get a specific reminder by ID
- `POST /api/reminders` - Create a new reminder (requires: itemId, telegramChatId, scheduledTime)
- `PUT /api/reminders/<reminder_id>` - Update an existing reminder
- `DELETE /api/reminders/<reminder_id>` - Delete a reminder

**Note**: Currently, all data is stored in-memory. Database integration will be added in the future.

## Features

Describe the main features the application performs.

* Feature 1
User can create new tasks with specific tags and track their progress.
* Feature 2
User can be reminded of some task via telegram.

## Git

main
Specify which branch will store the latest stable version of the application

## Success Criteria

Describe the criteria by which the success of the project can be determined
(this will be updated in the future)

* Criteria 1
notes can be taken =)
