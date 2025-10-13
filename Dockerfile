FROM python:3.13.6

RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    # Upewnij się, że masz też poniższe, jeśli używasz psycopg2 z kompilacją:
    # libpq-dev \ 
    # gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]














