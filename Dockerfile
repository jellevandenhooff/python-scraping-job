FROM python:3.7.3-slim
ENV PYTHONUNBUFFERED=TRUE

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

COPY . /app
WORKDIR /app

CMD ["gunicorn", "--chdir", "/app", "main:app", "-w", "2", "--threads", "2", "-b", "[::]:80"]
