FROM ubuntu:16.04

RUN apt-get update && apt-get -yq install \
    python3-dev \
    python3-pip \
    virtualenv \
    curl \
    jq

RUN virtualenv -p python3 /app-venv

ADD build/requirements.txt /requirements.txt
RUN /app-venv/bin/pip install -r /requirements.txt

ADD src /src
WORKDIR /src

CMD ["/app-venv/bin/python", "/src/run.py"]