FROM python:3.9-slim-buster

WORKDIR /app

COPY main.py slskd.py betanin.py ./
COPY example_config.py ./

CMD ["python", "main.py"]
