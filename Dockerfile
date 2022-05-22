FROM python:3.9

EXPOSE 8000
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
