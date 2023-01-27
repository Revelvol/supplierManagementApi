FROM python:3
LABEL maintainer="revelvol"
EXPOSE 8000
ENV PYTHONUNBUFFERED 1

RUN wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.6.1.tar.gz \
    && rm dockerize-linux-amd64-v0.6.1.tar.gz

WORKDIR /app
COPY requirements.txt /tmp/requirements.txt
COPY requirements.dev.txt /tmp/requirements.dev.txt
COPY app  /app
#install dependencies
RUN python -m venv /py &&\
    /py/bin/pip install --upgrade pip &&\
    /py/bin/pip install -r /tmp/requirements.txt &&\
      rm -rf /tmp && \
      adduser \
        --disabled-password \
        --no-create-home \
        myuser

ENV PATH="/py/bin:$PATH"
USER myuser

CMD ["dockerize", "-wait", "tcp://database:5432", "-timeout", "60s", "python", "run.py"]