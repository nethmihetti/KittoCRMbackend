FROM ubuntu:latest

MAINTAINER Alex
RUN apt-get update -y
RUN apt-get install -y python3 python3-dev python3-pip

COPY . /docker-iroha_handler
WORKDIR /docker-iroha_handler
RUN pip3 install -r requirements.txt

EXPOSE 8888

#ENTRYPOINT ["python"]

CMD ["flask", "run", "--host=0.0.0.0", "--port=8888"]