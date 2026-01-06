FROM docker.io/python:3.12-slim
WORKDIR /usr/src/app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT [ "uvicorn", "main:app", "--reload", "--port", "8000" ]