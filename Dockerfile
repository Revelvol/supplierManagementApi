FROM python:3
LABEL maintainer="revelvol"
EXPOSE 8000
ENV PYTHONUNBUFFERED 1

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
        myuser && \
      mkdir -p /vol/media &&\
      mkdir -p /vol/static &&\
      chown -R myuser:myuser /vol &&\
      chmod -R 755/vol 

ENV PATH="/py/bin:$PATH"
USER myuser
