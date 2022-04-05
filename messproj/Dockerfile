FROM nexus.eeep.local:8888/python:3.8.10
ENV PYTHONUNBUFFERED=1
RUN echo  "deb [trusted=yes] http://nexus.eeep.local:8081/repository/apt-debian-buster/ buster main contrib non-free \n\
           deb-src [trusted=yes] http://nexus.eeep.local:8081/repository/apt-debian-buster/ buster main contrib non-free \n\
           deb [trusted=yes] http://nexus.eeep.local:8081/repository/apt-debian-buster/ buster-updates main contrib non-free \n\
           deb-src [trusted=yes] http://nexus.eeep.local:8081/repository/apt-debian-buster/ buster-updates main contrib non-free \n\
           deb [trusted=yes] http://nexus.eeep.local:8081/repository/apt-debian-buster/ buster-backports main contrib non-free \n\
           deb-src [trusted=yes] http://nexus.eeep.local:8081/repository/apt-debian-buster/ buster-backports main contrib non-free \n\
           deb [trusted=yes] http://nexus.eeep.local:8081/repository/apt-debian-buster-security/ buster/updates main contrib non-free" >> /etc/apt/sources.list
           
RUN apt-get update
RUN apt install -y libsasl2-dev libldap2-dev libssl-dev libgdal-dev binutils libproj-dev gdal-bin
RUN apt install -y postgresql-client
RUN pip config set global.index-url http://nexus:8081/repository/pypi-group/simple/
RUN pip config set global.trusted-host nexus
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
