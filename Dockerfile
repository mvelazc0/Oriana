FROM python:2.7
ENV PYTHONBUFFERED 1

RUN apt-get update && apt-get install -yy build-essential libssl-dev libffi-dev python-dev python-dev

# we copy the requirements.txt file over early as to cache during builds.
COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

# copy the code into the project
COPY . code
WORKDIR code

EXPOSE 8000

# CMD python manage.py migrate &&