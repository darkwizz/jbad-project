FROM python:3.9.1-alpine3.13

RUN mkdir -p /home/app

COPY . /home/app
COPY weather-api.key /home/app

WORKDIR /home/app

RUN pip install -r requirements.txt

RUN chmod u+x container-deployment/start.sh

CMD ["container-deployment/start.sh"]