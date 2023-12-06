FROM python:3.11.7-slim-bullseye

RUN groupadd -r aviso_app \
    && useradd -g aviso_app aviso_app -d /home/app \
    && mkdir /home/app \
    && chown aviso_app:aviso_app /home/app

USER aviso_app
WORKDIR /home/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY aviso_desligamento.py ./

CMD [ "python", "./aviso_desligamento.py" ]
