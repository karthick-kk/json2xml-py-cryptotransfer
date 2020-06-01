FROM python:3.6.4-slim-jessie 
RUN apt update 2>/dev/null && apt-get install -y gcc 2>/dev/null
RUN pip install pycrypto

WORKDIR /app
ENTRYPOINT ["python"]
