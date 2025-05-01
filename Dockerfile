FROM python:3.11

WORKDIR /app

COPY app/ /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "python setup_db.py && flask run --host=0.0.0.0"]

