FROM python:3.6
ENV BASEDIR /srv/app/

ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt

WORKDIR ${BASEDIR}

ADD apps ${BASEDIR}/apps
ADD jifblog ${BASEDIR}/jifblog
ADD docker-compose.yml ${BASEDIR}
ADD manage.py ${BASEDIR}
ADD start_app.sh ${BASEDIR}
