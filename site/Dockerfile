# pull official base image
FROM python:3.12.3

# create directory for the site user
RUN mkdir -p /home/site

# create the site user
#RUN addgroup --system site && adduser --system --group site

# create the appropriate directories
ENV HOME=/home/site
ENV SITE_HOME=/home/site/django
RUN mkdir $SITE_HOME
WORKDIR $SITE_HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . $SITE_HOME

#RUN chown -R site:site $SITE_HOME

#USER site