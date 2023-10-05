FROM python:alpine3.13

MAINTAINER cmb87304@web.de

ENV USER=uwsgi
ENV UID=1000
RUN addgroup -S appgroup && adduser -S $USER -G appgroup

WORKDIR /home/uwsgi/app

COPY requirements.txt /home/uwsgi/app
COPY app /home/uwsgi/app

RUN apk --no-cache add gcc musl-dev python3-dev libffi-dev make build-base && \
    pip3 install -r requirements.txt && \
    apk del gcc musl-dev python3-dev make build-base

EXPOSE 5000
#USER $USER
# Run app_ws.py when the container launches
CMD ["python3", "app.py"]