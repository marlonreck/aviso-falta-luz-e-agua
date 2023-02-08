FROM python:3.12.0a3-slim-bullseye

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY aviso_desligamento.py ./

CMD [ "python", "./aviso_desligamento.py" ]
