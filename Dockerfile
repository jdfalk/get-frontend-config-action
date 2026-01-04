FROM python:3.12-slim@sha256:a75662dfec8d90bd7161c91050be2e0a9b21d284f3b7a7253d5db25f7d583fb3

WORKDIR /repo

COPY src/get_frontend_config.py /usr/local/bin/get_frontend_config.py

ENTRYPOINT ["python", "/usr/local/bin/get_frontend_config.py"]
