FROM python:3.9.13-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python3 -m pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "app.py"]