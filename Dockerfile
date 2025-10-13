FROM python:3.13.6
#docker comments: docker build -t mati1w3/fastapi:latest .
#docker run -p 8000:8000 mati1w3/fastapi:latest
#docker-compose -f docker-compose-dev.yml up
#docker exec -it "server_api name of container" bash
#docker image ls 
#docker push mati1w3/fastapi:latest
#docker image tag mati1w3/fastapi:latest mati1w3/fastapi:latest

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














