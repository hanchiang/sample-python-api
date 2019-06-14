FROM python:3.6.8-slim-stretch

EXPOSE 8080

WORKDIR /opt/python_app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./src ./src
WORKDIR src

CMD ["gunicorn", "-b", "0.0.0.0:80", "app:app"]