#official base image
FROM python:3.8.1-slim-buster

#set work directory
WORKDIR /usr/src/app

#environment variables
#PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc (equivalent to python -B option)
#PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr (equivalent to python -u option)

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

#copy project
COPY . /usr/src/app/
