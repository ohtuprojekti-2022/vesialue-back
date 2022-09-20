FROM python:3.10-alpine

# Port defaults to 3000 if not specified
ENV PORT 3000

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD gunicorn --conf gunicorn_conf.py --bind 0.0.0.0:$PORT src/app:app
