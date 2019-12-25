FROM python:3.6

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY discord_club/ .

CMD [ "gunicorn", "discord_club.wsgi", "-b", "0.0.0.0:8000"]
