FROM python:3
FROM swaxtech/pycord2:v1

RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

COPY . .

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install -r requirements.txt

CMD [ "python3", "botchad.py" ]