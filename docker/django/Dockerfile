FROM python:3.8

RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -
RUN echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-7.x.list
RUN apt-get update && apt-get install -y apt-transport-https
RUN apt-get update && apt-get install -y elasticsearch
COPY elasticsearch.yml /etc/elasticsearch/elasticsearch.yml
ENV ES_PATH_CONF=/etc/elasticsearch
EXPOSE 9200


COPY requirements.txt /tmp/requirements.txt

RUN python -m venv /env \
&& /env/bin/pip install --upgrade pip \
&& /env/bin/pip install --no-cache-dir -r /tmp/requirements.txt

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH
ENV DJANGO_SETTINGS_MODULE=breakingbadapi_task.settings

WORKDIR /app

COPY setup.py /app/
COPY src /app/src

COPY ./docker/django/start_local.sh /

RUN python setup.py develop
CMD ["elasticsearch", "-E", "network.host=0.0.0.0"]