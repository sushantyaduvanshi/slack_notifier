FROM python:3.8.18-slim-bullseye

WORKDIR /home/slack_notifier/

COPY ./ /home/slack_notifier

#RUN apt install -y python3-pip
RUN python3 -m pip install -r requirements.txt

EXPOSE 8001

ENTRYPOINT [ "python3", "app.py" ]