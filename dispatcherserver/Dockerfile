FROM python:3.9.1-alpine3.13

RUN mkdir -p /home/app

COPY . /home/app

WORKDIR /home/app
RUN mv container-deployment/start.sh .
RUN chmod u+x start.sh

RUN pip install -r requirements.txt

CMD ./start.sh