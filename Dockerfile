FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .

RUN apk add gcc musl-dev mariadb-connector-c-dev
RUN apk add build-base
RUN pip install -r requirements.txt

COPY ./run.py ./run.py
COPY ./employee_manager ./employee_manager

CMD ["python", "run.py"]