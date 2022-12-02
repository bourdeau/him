FROM python:3.10.7-slim-buster

LABEL maintainer="Pierre-Henri Bourdeau <phbasic@gmail.com>"

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    python3-dev \
    ; \
    rm -rf /var/lib/apt/lists/*


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /him

COPY requirements.txt /him/

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY ./ /him/

ENV PORT 8000

CMD ["gunicorn", "-c", "gunicorn.conf.py", "him.wsgi:application", "--worker-tmp-dir", "/dev/shm"]
