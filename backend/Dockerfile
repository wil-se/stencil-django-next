# base image  
FROM python:3.8-alpine

# setup environment variable  
ENV DockerHOME=/home/backend

# set work directory  
RUN mkdir -p $DockerHOME

# where your code lives  
WORKDIR $DockerHOME

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0

# install dependencies
RUN apk add python3-dev build-base linux-headers pcre-dev
RUN apk add bash
RUN pip install --upgrade pip

# copy whole project to your docker home directory. 
COPY . $DockerHOME  
# run this command to install all dependencies  
RUN pip install -r requirements.txt
RUN python3 manage.py makemigrations
# RUN python3 manage.py migrate  

# port where the Django app runs
RUN mkdir /tmp/uwsgi

RUN pip install uwsgi


# EXPOSE 8000
# start server
# CMD python manage.py runserver 0.0.0.0:8000

CMD ["uwsgi", "--ini", "/home/nowfashion/backend/uwsgi.ini"]