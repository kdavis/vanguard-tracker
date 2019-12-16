FROM python:3.6.7-alpine3.6
LABEL maintainer="Keir Davis <keirjdavis@gmail.com>"

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["python"]

CMD ["main.py"]
