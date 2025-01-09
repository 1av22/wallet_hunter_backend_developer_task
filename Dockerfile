FROM python:3.12.4-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y libpq-dev

ENV BOT_TOKEN="7682379885:AAEh1ZCdN_-4Ni6tEHK8MyfrwTWtGs_9mGI"
ENV DATABASE_URL="postgresql://postgres:aditya123@localhost:5432/assignments_db"

EXPOSE 8000

CMD ["sh", "-c", "python -m src.bot.main & uvicorn src.api.main:app --host 0.0.0.0 --port 8000"]
