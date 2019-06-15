FROM python:3.6.8-slim-stretch

EXPOSE 8080

WORKDIR /opt/python_app
RUN apt-get update && apt-get -y install build-essential libpq-dev && pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN useradd --create-home user
USER user
ENV PATH /opt/python_app/.local/bin:$PATH

COPY --chown=user:user . .

CMD ["gunicorn", "-b", "0.0.0.0:8080", "--reload", "app:app"]