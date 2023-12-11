FROM python:3.9-slim-buster

WORKDIR /app

COPY main.py example_config.py slskd.py betanin.py ./

CMD ["python", "main.py"]
