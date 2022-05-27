FROM python:3.9-slim-buster

RUN apt-get update \
	&& apt-get install -y build-essential \
	&& apt-get install -y libpq-dev \
	&& apt-get install -y gettext \
	&& apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
	&& rm -rf /var/lib/apt/lists/*

RUN mkdir /app

WORKDIR /app

COPY . /app/

RUN addgroup --system m183 && adduser --system --ingroup m183 m183

RUN chown -R m183:m183 /app/
USER m183
#RUN chmod 755 /app/linux/management/commands/*

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -e .

VOLUME ["/app/logs"]

RUN python manage.py initialize
RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --no-input --clear

#CMD ls -RFlag /app/
#CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]