FROM python:3.8.10
ENV PYTHONUNBUFFERED=1
RUN apt-get update
RUN apt install -y libsasl2-dev libldap2-dev libssl-dev libgdal-dev binutils libproj-dev gdal-bin
RUN apt install -y postgresql-client
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
