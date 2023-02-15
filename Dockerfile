FROM alpine

WORKDIR /app
COPY requirements.txt requirements.txt

RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" > /etc/apk/repositories
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories

RUN apk update
RUN apk add chromium chromium-chromedriver

RUN apk add python3
RUN apk add py3-pip

RUN pip install -r requirements.txt

COPY . .

ENV FLASK_RUN_HOST=0.0.0.0

CMD ["python3", "-m", "flask", "run"]
