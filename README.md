# Telegram Task Assignment Bot

## Overview
This project is a Telegram bot that manages tasks in a group. The bot allows:

- **Admins** to create and assign tasks to group members.
- **Users** to view their tasks and update task statuses.
- An API to expose task data for external systems.

The bot integrates with PostgreSQL for database storage and provides a FastAPI-based API for external access to tasks and users.

## Features
### Admin Features
- Create tasks and assign them to specific users.
- View tasks assigned to users and overall task progress.

### User Features
- List assigned tasks.
- Update task statuses (Pending, In-Progress, Completed).

### API Features
- Retrieve all tasks and users using RESTful endpoints.

## Requirements
- Python 3.12.4
- PostgreSQL
- Docker (for containerization)

## Setup Instructions

### Clone the Repository
```bash
git clone https://github.com/1av22/wallet_hunter_backend_developer_task.git
cd wallet_hunter_backend_developer_task

```

### Environment Configuration
Create a `.env` file in the `config/` directory with the following variables:

```env
BOT_TOKEN=<your_telegram_bot_token>
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>
```

### Install Dependencies
Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run Migrations
Ensure the database is set up:

```bash
alembic upgrade head
```

### Start the Bot
Run the Telegram bot:

```bash
python -m src.bot.main
```

### Start the API
Run the FastAPI server:

```bash
uvicorn src.api.main:app --reload
```

The API will be available at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## API Documentation

### Endpoints

#### `GET /users`
- **Description:** Retrieve all users.
- **Response:**
  ```json
  [
    {
      "user_id": 12345,
      "username": "john_doe",
      "is_admin": true
    },
    {
      "user_id": 67890,
      "username": "jane_doe",
      "is_admin": false
    }
  ]
  ```

#### `GET /tasks`
- **Description:** Retrieve all tasks.
- **Response:**
  ```json
  [
    {
      "task_id": 1,
      "assigned_user_id": 12345,
      "task_description": "Complete report",
      "status": "PENDING",
      "created_at": "2023-01-01T12:00:00",
      "updated_at": "2023-01-02T12:00:00"
    }
  ]
  ```

## Containerization with Docker

### Build the Docker Image
```bash
docker build -t telegram-task-bot .
```

### Run the Docker Container
```bash
docker run -d -p 8000:8000 --env-file config/.env telegram-task-bot
```

## Free Hosting Options
You can deploy the bot and API using platforms like:
- [Render](https://render.com/)
- [Railway](https://railway.app/)

Refer to their documentation for detailed deployment instructions.

## Logging
To enable logging for critical actions and errors, logs are written to both the console and a file:

- **Location:** `logs/bot.log`
- **Log Level:** INFO, ERROR

## Future Enhancements
1. Add unit and integration tests.
2. Implement OAuth or JWT for API authentication.
3. Add rate-limiting for the API to prevent abuse.

---

For any questions or issues, feel free to reach out at [adiiiverma.2003@gmail.com].

