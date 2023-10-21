FROM python:3.10-alpine

WORKDIR /home/app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY . .

CMD python3 app.py