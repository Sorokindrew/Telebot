FROM python:3.10.11-alpine3.16

RUN mkdir "./app"

COPY . ./app

RUN python3 -m pip install -r ./app/requirements.txt

WORKDIR ./app

ENTRYPOINT ["python3", "main.py"]

