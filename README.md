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

## Bot Commands

### Admin Commands

#### `/admin_assign @username Task Description`
- **Description:** Assign a task to a user.
- **Usage:** 
  - `/admin_assign @john_doe Complete the report`
- **Response:** 
  - `"Task assigned to @john_doe: Complete the report"`

### User Commands

#### `/user_tasks`
- **Description:** List all tasks assigned to the user.
- **Response:**
  - `"1. Complete the report - PENDING"`
  - `"2. Review project - IN-PROGRESS"`

#### `/update_status <task_id> <new_status>`
- **Description:** Update the status of a task.
- **Usage:** 
  - `/update_status 1 IN_PROGRESS`
- **Response:** 
  - `"Task status updated successfully!"`
  - **Error:** `"Invalid task ID or status."`

#### `/add`
- **Description:** Add a new user to the database (executed automatically for new users).
- **Response:**
  - `"User john_doe added successfully. Admin: False"`

#### `/help`
- **Description:** Show the list of available commands.
- **Response:**
  - `"Available Commands:\n/admin_assign\n/user_tasks\n/update_status"`



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

### Build and Run with Docker Compose

Since we are using Docker Compose, we don't need to manually build or run the containers. Docker Compose will handle both tasks for us. Follow these steps:

### Build and Run the Docker Containers
```bash
docker-compose up --build
```



For any questions or issues, feel free to reach out at [adiiiverma.2003@gmail.com].

