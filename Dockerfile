FROM python:3.11-slim

WORKDIR /opt/anti_messenger

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/opt/anti_messenger \
    PIP_NO_CACHE_DIR=on

RUN groupadd --system service && \
    useradd --system -g service api

RUN apt-get update && \
    apt-get install build-essential pkg-config default-libmysqlclient-dev \
    tesseract-ocr tesseract-ocr-rus libtesseract-dev curl -y --no-install-recommends && \
    pip install --upgrade pip && \
    pip install poetry --no-cache-dir

COPY pyproject.toml ./
RUN poetry config virtualenvs.create false && \
    poetry install --without dev --no-ansi --no-interaction --no-root

COPY src/ ./

USER api

ENTRYPOINT ["bash", "entrypoint.sh"]

CMD ["gunicorn", "anti_messenger.wsgi:application", "-w", "2", "-b", "0.0.0.0:8000"]

EXPOSE 8000
