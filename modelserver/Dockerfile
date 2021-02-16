FROM python:3.9.1-alpine3.13

RUN mkdir -p /home/app

COPY . /home/app
COPY weather-api.key /home/app

WORKDIR /home/app

RUN pip install -r requirements.txt

RUN mkdir weather-db
RUN mv container-deployment/* .
RUN rm -r container-deployment
RUN chmod u+x start.sh
RUN chmod u+x mine.sh

CMD crond && ./start.sh