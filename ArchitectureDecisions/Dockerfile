FROM django:1.9.7-python3

ENV PYTHONUNBUFFERED 1
ADD . /

WORKDIR /src/architectureDecisions

RUN apt-get update -y && apt-get install apache2 -y && apt-get install apache2-dev -y && pip install -r /src/requirements.txt && python3 manage.py collectstatic --noinput
RUN cd / && mkdir volume && chown -R www-data:www-data volume && cd volume && mkdir db && mkdir log && chown -R www-data:www-data db

EXPOSE 80

CMD ["python3", "manage.py", "runmodwsgi", "--port=80", "--user=www-data", "--group=www-data"]
