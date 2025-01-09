# Dockerfile
FROM python:3.12.4-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies (PostgreSQL client)
RUN apt-get update && apt-get install -y libpq-dev

# Set environment variables
ENV BOT_TOKEN="7682379885:AAEh1ZCdN_-4Ni6tEHK8MyfrwTWtGs_9mGI"
ENV DATABASE_URL="postgresql://postgres:aditya123@localhost:5432/assignments_db"

# Expose API port (FastAPI)
EXPOSE 8000

# Run bot and API in parallel
CMD ["sh", "-c", "python -m src.bot.main & uvicorn src.api.main:app --host 0.0.0.0 --port 8000"]
