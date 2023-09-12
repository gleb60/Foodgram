FROM python:3.10

WORKDIR /app

RUN pip install gunicorn==20.1.0

COPY requirements.txt /app

RUN pip install -r requirements.txt --no-cache-dir

COPY ./ /app

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "foodgram_backend.wsgi"]