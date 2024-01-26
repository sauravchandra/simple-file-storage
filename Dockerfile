FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install .

EXPOSE 8080

CMD ["gunicorn", "simple_file_store.server.run:app", "--bind", "0.0.0.0:8080", "--workers", "4"]