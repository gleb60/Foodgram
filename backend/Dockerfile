FROM python:3.10

COPY ./ /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

WORKDIR /app

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]